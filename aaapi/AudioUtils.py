import numpy as np
import librosa
import crepe
from scipy.signal import periodogram


def split(audio, top_db=25, min_duration=None):
    audio_split = librosa.effects.split(audio, top_db=top_db)
    if min_duration:
        min_len = min_duration
        n_intv_idx = list()
        prev_index = None
        index_f, index_l = None, None
        for index_f, index_l in audio_split:
            if prev_index is None:
                prev_index = index_f
            if index_l - prev_index > min_len:
                n_intv_idx += [[prev_index, index_l]]
                prev_index = None

        if index_l is not None and n_intv_idx[-1][1] != index_l:
            n_intv_idx += [[prev_index, index_l]]
        return n_intv_idx
    return audio_split


def audio_features(audio, sr):
    mfcc = librosa.feature.mfcc(audio, sr=sr, n_mels=12)
    spec_ent = spectral_entropy(audio, sf=100)
    columns = (
        ['spectral entropy']
        + ['mel {} mean'.format(i) for i in range(12)]
        + ['mel {} q1'.format(i) for i in range(12)]
        + ['mel {} q2'.format(i) for i in range(12)]
        + ['mel {} q3'.format(i) for i in range(12)]
        + ['mel {} std'.format(i) for i in range(12)]
    )
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)
    mfcc_q1 = np.percentile(mfcc, 0.25, axis=1)
    mfcc_q2 = np.median(mfcc, axis=1)
    mfcc_q3 = np.percentile(mfcc, 0.75, axis=1)
    au_features = (
        [spec_ent]
        + list(mfcc_mean)
        + list(mfcc_q1)
        + list(mfcc_q2)
        + list(mfcc_q3)
        + list(mfcc_std)
    )
    return au_features, columns


def estimate_f0(audio, sr):
    def f0_dict(time, frequency, confidence, activation):
        return dict(
            time=time,
            freq=frequency,
            conf=confidence,
        )

    f0_data = f0_dict(*crepe.predict(audio, sr, viterbi=True))
    return f0_data


def loadwav(*args, sr=44100, **kwargs):
    return librosa.core.load(*args, sr=sr, **kwargs)


def spectral_entropy(x, sf, nperseg=None, normalize=False):
    """
    Adapted from: https://raphaelvallat.com/entropy/build/html/_modules/entropy/entropy.html#spectral_entropy
    Spectral Entropy.

    Parameters
    ----------
    x : list or np.array
        One-dimensional time series of shape (n_times)
    sf : float
        Sampling frequency, in Hz.
    method : str
        Spectral estimation method:

        * ``'fft'`` : Fourier Transform (:py:func:`scipy.signal.periodogram`)
        * ``'welch'`` : Welch periodogram (:py:func:`scipy.signal.welch`)
    nperseg : int or None
        Length of each FFT segment for Welch method.
        If None (default), uses scipy default of 256 samples.
    normalize : bool
        If True, divide by log2(psd.size) to normalize the spectral entropy
        between 0 and 1. Otherwise, return the spectral entropy in bit.

    Returns
    -------
    se : float
        Spectral Entropy

    Notes
    -----
    Spectral Entropy is defined to be the Shannon entropy of the power
    spectral density (PSD) of the data:

    .. math:: H(x, sf) =  -\\sum_{f=0}^{f_s/2} P(f) log_2[P(f)]

    Where :math:`P` is the normalised PSD, and :math:`f_s` is the sampling
    frequency.

    References
    ----------
    Inouye, T. et al. (1991). Quantification of EEG irregularity by
    use of the entropy of the power spectrum. Electroencephalography
    and clinical neurophysiology, 79(3), 204-210.

    https://en.wikipedia.org/wiki/Spectral_density

    https://en.wikipedia.org/wiki/Welch%27s_method

    Examples
    --------
    Spectral entropy of a pure sine using FFT

    >>> from entropy import spectral_entropy
    >>> import numpy as np
    >>> sf, f, dur = 100, 1, 4
    >>> N = sf * dur # Total number of discrete samples
    >>> t = np.arange(N) / sf # Time vector
    >>> x = np.sin(2 * np.pi * f * t)
    >>> np.round(spectral_entropy(x, sf, method='fft'), 2)
    0.0
    """
    x = np.array(x)
    # Compute and normalize power spectrum
    _, psd = periodogram(x, sf)
    psd_norm = np.divide(psd, psd.sum())
    se = -np.multiply(psd_norm, np.log2(psd_norm)).sum()
    if normalize:
        se /= np.log2(psd_norm.size)
    return se

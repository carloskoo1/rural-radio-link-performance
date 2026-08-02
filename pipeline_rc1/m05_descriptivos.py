
import pandas as pd


def calcular_descriptivos(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped = df.groupby(
        ["escenario", "frecuencia_mhz", "ancho_canal_mhz"],
        as_index=False,
    )

    base = grouped.agg(
        N=("escenario", "size"),
        Días=("fecha", "nunique"),
        RSSI_media=("rssi_dl", "mean"),
        RSSI_DE=("rssi_dl", "std"),
        RSSI_Q1=("rssi_dl", lambda s: s.quantile(0.25)),
        RSSI_Q3=("rssi_dl", lambda s: s.quantile(0.75)),
        SNR_media=("snr_dl", "mean"),
        SNR_DE=("snr_dl", "std"),
        MCS_media=("mcs_dl", "mean"),
        MCS_DE=("mcs_dl", "std"),
        Throughput_media=("throughput_dl", "mean"),
        Throughput_DE=("throughput_dl", "std"),
        Throughput_mediana=("throughput_dl", "median"),
    )
    base["RSSI_RIC"] = base["RSSI_Q3"] - base["RSSI_Q1"]

    signal = base[
        [
            "escenario", "frecuencia_mhz", "ancho_canal_mhz", "N", "Días",
            "RSSI_media", "RSSI_DE", "RSSI_RIC",
            "SNR_media", "SNR_DE", "MCS_media", "MCS_DE",
        ]
    ].rename(columns={
        "escenario": "Escenario",
        "frecuencia_mhz": "Frecuencia (MHz)",
        "ancho_canal_mhz": "Canal (MHz)",
        "RSSI_media": "RSSI media (dBm)",
        "RSSI_DE": "RSSI DE (dB)",
        "RSSI_RIC": "RSSI RIC (dB)",
        "SNR_media": "SNR media (dB)",
        "SNR_DE": "SNR DE",
        "MCS_media": "MCS media",
        "MCS_DE": "MCS DE",
    }).round(3)

    throughput = base[
        [
            "escenario", "frecuencia_mhz", "ancho_canal_mhz",
            "Throughput_media", "Throughput_DE", "Throughput_mediana",
        ]
    ].rename(columns={
        "escenario": "Escenario",
        "frecuencia_mhz": "Frecuencia (MHz)",
        "ancho_canal_mhz": "Canal (MHz)",
        "Throughput_media": "Throughput media (Mb/s)",
        "Throughput_DE": "Throughput DE",
        "Throughput_mediana": "Throughput mediana (Mb/s)",
    }).round(3)

    return signal, throughput


def texto_descriptivos(signal: pd.DataFrame, throughput: pd.DataFrame) -> tuple[str, str, str, str]:
    intro_signal = (
        "Con el propósito de caracterizar el comportamiento del radioenlace, se "
        "examinaron RSSI, SNR y MCS para cada escenario."
    )
    best_rssi = signal.loc[signal["RSSI media (dBm)"].idxmax()]
    best_snr = signal.loc[signal["SNR media (dB)"].idxmax()]
    best_mcs = signal.loc[signal["MCS media"].idxmax()]
    interpretation_signal = (
        f"{best_rssi['Escenario']} presentó el mayor RSSI promedio "
        f"({best_rssi['RSSI media (dBm)']:.2f} dBm); "
        f"{best_snr['Escenario']} alcanzó el mayor SNR "
        f"({best_snr['SNR media (dB)']:.2f} dB); y "
        f"{best_mcs['Escenario']} registró el mayor MCS medio "
        f"({best_mcs['MCS media']:.2f})."
    )

    intro_th = (
        "La capacidad efectiva observada se examinó mediante el throughput descendente "
        "registrado durante el monitoreo."
    )
    valid = throughput.dropna(
        subset=["Throughput media (Mb/s)", "Throughput mediana (Mb/s)"]
    )
    best_mean = valid.loc[valid["Throughput media (Mb/s)"].idxmax()]
    best_median = valid.loc[valid["Throughput mediana (Mb/s)"].idxmax()]
    interpretation_th = (
        f"El mayor throughput medio correspondió a {best_mean['Escenario']} "
        f"({best_mean['Throughput media (Mb/s)']:.3f} Mb/s), mientras que la mayor "
        f"mediana se observó en {best_median['Escenario']} "
        f"({best_median['Throughput mediana (Mb/s)']:.2f} Mb/s). Esta métrica "
        "representa tráfico cursado y no capacidad nominal."
    )
    return intro_signal, interpretation_signal, intro_th, interpretation_th

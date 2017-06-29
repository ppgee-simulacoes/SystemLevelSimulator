import numpy as np
import matplotlib.pyplot as plt


class Results(object):
    """
    ADD description

    """

    def __init__(self):

        self.__snir_DL = []
        self.__snir_UL = []

    def add_snir(self, snir_vector_DL, snir_vector_UL):
        self.__snir_DL.append(snir_vector_DL)
        self.__snir_UL.append(snir_vector_UL)

    def plot_snir_cdf(self):
        ax_DL, val_DL = self._plot_cdf(self.__snir_DL)
        ax_UL, val_UL = self._plot_cdf(self.__snir_UL)

        ax_DL.set_xlabel("SNIR [dB]")
        ax_DL.set_ylabel("CDF of SNIR")
        ax_DL.set_title("SNIR for the Downlink")
        ax_DL.set_xlim([np.min(val_DL), np.max(val_DL)])
        ax_DL.set_ylim([0, 1])
        ax_DL.xaxis.grid(True)
        ax_DL.yaxis.grid(True)

        ax_UL.set_xlabel("SNIR [dB]")
        ax_UL.set_ylabel("CDF of SNIR")
        ax_UL.set_title("SNIR for the Uplink")
        ax_UL.set_xlim([np.min(val_UL), np.max(val_UL)])
        ax_UL.set_ylim([0, 1])
        ax_UL.xaxis.grid(True)
        ax_UL.yaxis.grid(True)

        return ax_DL, ax_UL

    def _plot_cdf(self, values_list):
        values = np.hstack(np.array(values_list))
        values = np.sort(values)
        prob_values = np.arange(0, len(values))/len(values)

        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)

        ax.plot(values, prob_values)

        return ax, values

    def reset(self):
        self.__snir_DL = []
        self.__snir_UL = []

    @property
    def snir_DL(self):
        return self.__snir_DL

    @property
    def snir_UL(self):
        return self.__snir_UL

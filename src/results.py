import numpy as np
import matplotlib.pyplot as plt


class Results(object):
    """
    ADD description

    """

    def __init__(self):

        self.__snir_DL = []
        self.__snir_UL = []
        self.__throughput_DL = []
        self.__throughput_UL = []

    def add_statistics(self, statistics_DL, statistics_UL):

        snir_vector_DL, throughput_DL = statistics_DL
        snir_vector_UL, throughput_UL = statistics_UL

        self.snir_DL.append(snir_vector_DL)
        self.snir_UL.append(snir_vector_UL)
        self.throughput_DL.append(throughput_DL)
        self.throughput_UL.append(throughput_UL)

    def plot_statistics_cdf(self):

        ax_snir_DL, snir_DL = self._plot_cdf(self.snir_DL)
        ax_snir_UL, snir_UL = self._plot_cdf(self.snir_UL)
        ax_tput_DL, tpt_DL = self._plot_cdf(self.throughput_DL)
        ax_tput_UL, tpt_UL = self._plot_cdf(self.throughput_UL)

        ax_snir_DL.set_xlabel("SNIR [dB]")
        ax_snir_DL.set_ylabel("CDF of SNIR")
        ax_snir_DL.set_title("SNIR for the Downlink")
        ax_snir_DL.set_xlim([np.min(snir_DL), np.max(snir_DL)])
        ax_snir_DL.set_ylim([0, 1])
        ax_snir_DL.xaxis.grid(True)
        ax_snir_DL.yaxis.grid(True)

        ax_snir_UL.set_xlabel("SNIR [dB]")
        ax_snir_UL.set_ylabel("CDF of SNIR")
        ax_snir_UL.set_title("SNIR for the Uplink")
        ax_snir_UL.set_xlim([np.min(snir_UL), np.max(snir_UL)])
        ax_snir_UL.set_ylim([0, 1])
        ax_snir_UL.xaxis.grid(True)
        ax_snir_UL.yaxis.grid(True)

        ax_tput_DL.set_xlabel("Throughput [bps]")
        ax_tput_DL.set_ylabel("CDF of Throughput")
        ax_tput_DL.set_title("Throughput for the Downlink")
        ax_tput_DL.set_xlim([np.min(tpt_DL), np.max(tpt_DL)])
        ax_tput_DL.set_ylim([0, 1])
        ax_tput_DL.xaxis.grid(True)
        ax_tput_DL.yaxis.grid(True)

        ax_tput_UL.set_xlabel("Throughput [bps]")
        ax_tput_UL.set_ylabel("CDF of Throughput")
        ax_tput_UL.set_title("Throughput for the Uplink")
        ax_tput_UL.set_xlim([np.min(tpt_UL), np.max(tpt_UL)])
        ax_tput_UL.set_ylim([0, 1])
        ax_tput_UL.xaxis.grid(True)
        ax_tput_UL.yaxis.grid(True)

        return ax_tput_UL, ax_snir_UL, ax_tput_DL, ax_snir_DL

    def _plot_cdf(self, values_list):
        values = np.hstack(np.array(values_list))
        values = np.sort(values)
        prob_values = np.arange(0, len(values))/len(values)

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)

        ax.plot(values, prob_values)

        return ax, values

    def reset(self):
        self.__snir_DL = []
        self.__snir_UL = []
        self.__throughput_DL = []
        self.__throughput_UL = []

    @property
    def snir_DL(self):
        return self.__snir_DL

    @property
    def snir_UL(self):
        return self.__snir_UL

    @property
    def throughput_DL(self):
        return self.__throughput_DL

    @property
    def throughput_UL(self):
        return self.__throughput_UL
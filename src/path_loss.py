import numpy as np
from support.enumeration import PropagationModel, PropagationEnvironment


class PathLoss (object):
    """
    ADD description

    """

    def __init__(self, parameters, random_state):

        self.__model = parameters.propagation_model

        self.__random_state = random_state

        if self.__model == PropagationModel.GENERIC:
            self.__d0 = parameters.d0
            self.__pl_d0 = parameters.pl_d0
            self.__alpha = parameters.pl_alpha

        elif self.__model == PropagationModel.OKUMURA_COST:
            self.__t_height = parameters.bs_height
            self.__r_height = parameters.ms_height
            self.__environment = parameters.propagation_environment

        self.__frequency = parameters.frequency

        if parameters.shadowing:
            self.__pl_sigma = parameters.pl_sigma
        else:
            self.__pl_sigma = None

    def calculate_path_loss(self, distance):
        if self.model == PropagationModel.GENERIC:
            path_loss = self.pl_generic(distance)
        elif self.model == PropagationModel.FREE_SPACE:
            path_loss = self.pl_free_space(distance)
        elif self.model == PropagationModel.OKUMURA_COST:
            path_loss = self.pl_okumura_cost(distance)

        if self.pl_sigma:
            path_loss += self.get_shadowing()

        return path_loss

    def pl_generic(self, distance):
        path_loss = self.pl_d0 + 10 * self.alpha * np.log10(distance/self.d0)
        return path_loss

    def pl_free_space(self, distance):
        frequency_GHz = self.frequency/1e9
        distance_km = distance/1e3
        path_loss = 20 * np.log10(frequency_GHz) + 20 * np.log10(distance_km) + 92.44
        return path_loss

    def pl_okumura_cost(self, distance):
        frequency_MHz = self.frequency/1e6
        distance_km = distance/1e3
        if self.environment == PropagationEnvironment.DENSE_URBAN:
            if frequency_MHz <= 300:
                a = 8.29 * np.log10((1.54 * self.r_height) ** 2) - 1.1
            else:
                a = 3.2 * np.log10((11.75 * self.r_height) ** 2) - 4.97
        else:
            a = (1.1 * np.log10(frequency_MHz) - 0.7) * self.__r_height - (1.56 * np.log10(frequency_MHz) - 0.8)

        if frequency_MHz <= 1500:
            path_loss_urban = 69.55 + 26.6 * np.log10(frequency_MHz) - 13.82 * np.log10(self.__t_height) - a \
                              - (44.9 - 6.55 * np.log10(self.t_height)) * np.log10(distance_km)
        elif frequency_MHz <= 2000:
            path_loss_urban = 46.3 + 33.9 * np.log10(frequency_MHz) - 13.82 * np.log10(self.__t_height) - a \
                              - (44.9 - 6.55 * np.log10(self.t_height)) * np.log10(distance_km)
            if self.environment == PropagationEnvironment.DENSE_URBAN:
                path_loss_urban += 3

        if self.environment == PropagationEnvironment.DENSE_URBAN or self.environment == PropagationEnvironment.URBAN:
            path_loss = path_loss_urban
        elif self.environment == PropagationEnvironment.SUBURBAN:
            path_loss = path_loss_urban - 2 * ((np.log10(frequency_MHz/28)) ** 2) - 5.4
        elif self.environment == PropagationEnvironment.RURAL:
            path_loss = path_loss_urban - 4.78 * (np.log10(frequency_MHz) ** 2) \
                        - 18.33 * np.log10(frequency_MHz) - 40.98

        return path_loss

    def get_shadowing(self):
        return self.random_state.normal(0, self.pl_sigma)


    @property
    def model(self):
        return self.__model

    @property
    def random_state(self):
        return self.__random_state

    @property
    def d0(self):
        return self.__d0

    @property
    def pl_d0(self):
        return self.__pl_d0

    @property
    def alpha(self):
        return self.__alpha

    @property
    def pl_sigma(self):
        return self.__pl_sigma

    @property
    def frequency(self):
        return self.__frequency

    @property
    def t_height(self):
        return self.__t_height

    @property
    def r_height(self):
        return self.__r_height

    @property
    def environment(self):
        return self.__environment

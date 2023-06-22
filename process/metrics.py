# -*- processing: LCONNECT -*-

import numpy as np


class metric:

    def SAM(self, image, r_spectrum, nb):
        """
        It calculates the Spectral Angle Mapper metric:
        :param image: array with "nb" bands stacked. Bands with surface reflectance;
        :param r_spectrum: reference spectrum from the river;
        :param nb: number of bands;
        :return: array with SAM values.
        """
        # List data:
        l_multiply = []
        l_power_t = []
        l_power_r = []
        # Calculates the products:
        for num in range(0, nb):
            multiply_ = np.multiply(image[num], float(r_spectrum.iloc[[num]]))
            power_t_ = np.power(image[num], 2)
            power_r_ = np.power(float(r_spectrum.iloc[[num]]), 2)
            l_multiply.append(multiply_)
            l_power_t.append(power_t_)
            l_power_r.append(power_r_)
        # Sums the data:
        sum_m_ = np.sum(l_multiply, axis=0)
        sum_t_ = np.sum(l_power_t, axis=0)
        sum_r_ = np.sum(l_power_r, axis=0)
        # Calculates the SAM algorithm:
        factor_1 = np.sqrt(np.multiply(sum_t_, sum_r_))
        factor_2 = np.divide(sum_m_, factor_1)
        sam_ = np.arccos(factor_2)
        return (sam_)


    def ED(self, image, r_spectrum, nb):
        """
        It calculates the Euclidian Distance metric:
        :param image: array with "nb" bands stacked. Bands with surface reflectance;
        :param r_spectrum: reference spectrum from the river;
        :param nb: number of bands;
        :return: array with ED values.
        """
        s_xy_ = []
        for i in range(0, nb):
            x_ = image[i]
            y_ = r_spectrum[i]
            z = (x_ - y_) ** 2
            s_xy_.append(z)
        # Calculates the ED:
        ed_ = np.sum(s_xy_, axis=0) ** (1/2)
        return (ed_)


    def SC(self, image, r_spectrum, nb):
        """
        It calculates the Spectral Correlation metric:
        :param image: array with "nb" bands stacked. Bands with surface reflectance;
        :param r_spectrum: reference spectrum from the river;
        :param nb: number of bands;
        :return: array with SC values.
        """
        a_multiply = []
        d_power = []
        f_power = []
        for i in range(0, nb):
            a_multiply .append(image[i] * r_spectrum[i])
            d_power.append(image[i] ** 2)
            f_power.append(r_spectrum[i] ** 2)
        # Calculates the SC:
        a_ = np.sum(a_multiply, axis=0)
        b_ = np.sum(image, axis=0)
        c_ = np.sum(r_spectrum)
        d_ = np.sum(d_power, axis=0)
        f_ = np.sum(f_power, axis=0)
        aa_ = (nb * a_) - (b_ * c_)
        bb_ = (nb * d_) - (b_ ** 2)
        cc_ = (nb * f_) - (c_ ** 2)
        dd_ = np.sqrt(bb_ * cc_)
        sc_ = aa_ / dd_
        return (sc_)


    def SID(self, image, r_spectrum, nb):
        """
        It calculates the Spectral Information Divergence metric:
        :param image: array with "nb" bands stacked. Bands with surface reflectance;
        :param r_spectrum: reference spectrum from the river;
        :param nb: number of bands;
        :return: array with SID values.
        """
        d_xy_ = []
        d_yx_ = []
        for i in range(0, nb):
            x_ = image[i]
            y_ = r_spectrum[i]
            # Probability measure:
            p_x_ = x_ / np.sum(image, axis=0)
            p_y_ = y_ / np.sum(r_spectrum)
            # Divergences:
            Dxy_ = p_x_ * (np.log10(p_x_ / p_y_))
            Dyx_ = p_y_ * (np.log10(p_y_ / p_x_))
            d_xy_.append(Dxy_)
            d_yx_.append(Dyx_)
        # SID:
        sid_ = np.sum(d_xy_, axis=0) + np.sum(d_yx_, axis=0)
        return (sid_)


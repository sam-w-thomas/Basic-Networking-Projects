from math import trunc

class EIGRP_Metric:
    """Basic EIGRP Metric Calculation Class
    :parameter arg1: Minimum Bandwidth on route
    :paramter arg2: Total Delay (in microseconds)
    :paramter arg3: Load [optional]
    :paramter arg4: Reliability [optional]
    :paramter arg5: Extended - Jitter and Energy [optional, wide metrics only]
    :paramter arg6: Set to True to use Wide Metrics
    :return: Prints metric when created.
    """

    def __init__(self, minbandwidth, delay, load=0, reliability=0, extended=0, wide=False):
        self._minbandwidth = minbandwidth
        self._delay = delay
        self._load = load
        self._reliability = reliability
        self._extended = extended

        self.set_k_values()

        if not wide:
            self._scalar = 256
        else:
            self._scalar = 65353

        self.calculate_metric()

    def set_k_values(self, k1=1, k2=0, k3=1, k4=0, k5=0, k6=0):
        """
        Used to define what is used in EIGRP calculations

        :param k1: Bandwidth
        :param k2: Bandwidth
        :param k3: Delay
        :param k4: Load
        :param k5: Reliability
        :param k6: Extended - Jitter and
        """
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._k4 = k4
        self._k5 = k5
        self._k6 = k6

    def calculate_metric(self):
        bandwidth = 10 ** 7 / self._minbandwidth
        load = self._load
        delay = self._delay / 10 #Wide metric delay, latency, has conflicting discussions. ENCOR study guide is used as reference
        if(self._k6 > 0):
            reliability = self._k5 / self._k6 + self._reliability
        else:
            reliability = 1


        self._metric = trunc(self._scalar * (((self._k1 * bandwidth) + ((self._k2 * bandwidth) / 256 - load) + (self._k3 * delay)) * reliability))

    @property
    def metric(self):
        return self._metric

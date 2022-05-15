import sys

#Print Progressbar in the command window
class ProgressBar:
    def __init__(self):
        """
        initialize
        """
        # standard out stream
        self.__stdout = sys.stdout
        # parameters
        self.__max = None
        self.__step = None
        self.__value = 0
        # style parameters
        self.__bar_length = 40
        self.__content_char = '█'
        self.__white_char = ' '
        self.__border_char = ('[', ']')
        self.__max_chars = 100
    
    def initialize(self, max_value, step):
        """
        initialize progress bar
        :param max_value: max value
        :param step: step
        :return:
        """
        assert isinstance(max_value, int)
        assert isinstance(step, int)
        # save parameters
        self.__max = max_value
        self.__step = step
        # init parameters
        self.__value = 0

    def refresh(self, state_info=None):
        """
        write state information to stdout
        :param state_info: state message
        :return:
        """
        # get number of symbols
        ss = min(self.__bar_length, self.__value * self.__bar_length // self.__max)
        # get chars
        cs = '{0}{1}{2}{3} {4}'.format(self.__border_char[0], self.__content_char * ss,
                                       self.__white_char * (self.__bar_length - ss), self.__border_char[1], state_info)
        # show state
        self.__stdout.write('\r')
        self.__stdout.write(cs)
        self.__stdout.flush()

    def update(self, state_info=None, increment=None):
        """
        update state information and refresh display
        :param increment: increment, default None
        :param state_info: state information
        :return:
        """
        # update current value
        if increment is None:
            self.__value += self.__step
        else:
            self.__value += increment
        # refresh
        self.refresh(state_info)

    def __call__(self, iter_obj):
        """
        initialize using a iterable object
        :param iter_obj: iterable object
        :return:
        """
        self.initialize(len(iter_obj), 1)
        return iter_obj
    
    def overlay_display(self, state_info):
        """
        hide progress bar and show state message
        :param state_info: state information
        :return:
        """
        self.__stdout.write('\r{0}{1}\n'.format(state_info, ' ' * (max(self.__max_chars - len(state_info), 0))))
        self.__stdout.flush()

    def overlay_display(self, state_info):
        """
        hide progress bar and show state message
        :param state_info: state information
        :return:
        """
        self.__stdout.write('\r{0}{1}\n'.format(state_info, ' ' * (max(self.__max_chars - len(state_info), 0))))
        self.__stdout.flush()

    def set_style(self, **kwargs):
        """
        set style of the progress bar
        :param kwargs: key words
        :return:
        """
        if 'bl' in kwargs:
            self.__bar_length = kwargs['bl']
        if 'cc' in kwargs:
            self.__content_char = kwargs['cc']
        if 'wc' in kwargs:
            self.__white_char = kwargs['wc']
        if 'bc' in kwargs:
            self.__border_char = kwargs['bc']
        if 'mc' in kwargs:
            self.__max_chars = kwargs['mc']
    
    @property
    def max_value(self):
        return self.__max

    @property
    def curr_value(self):
        return self.__value
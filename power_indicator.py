#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RF Signal Indicator
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio import zeromq
from gnuradio.fft import logpwrfft
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import threading



from gnuradio import qtgui

class power_indicator(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RF Signal Indicator", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RF Signal Indicator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "power_indicator")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.offset = offset = 0
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = variable_function_probe_0-offset
        self.samp_rate = samp_rate = 20000000
        self.rfgain = rfgain = 50
        self.freq = freq = 5.735e9
        self.averages = averages = 1000

        ##################################################
        # Blocks
        ##################################################
        self._rfgain_range = Range(0, 76, 1, 50, 200)
        self._rfgain_win = RangeWidget(self._rfgain_range, self.set_rfgain, 'rfgain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rfgain_win)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'tcp://192.168.8.248:50001', 100, False, -1, '')
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Peak Value: ' + ": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)
        def _variable_function_probe_0_probe():
          while True:

            val = self.blocks_probe_signal_x_0.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_variable_function_probe_0,val))
              except AttributeError:
                self.set_variable_function_probe_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (15))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
        self.uhd_usrp_source_0.set_gain(rfgain, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(True, 0)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate*0.45,
                1e6,
                window.WIN_HAMMING,
                6.76))
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=4096,
            ref_scale=2,
            frame_rate=30,
            avg_alpha=0.1,
            average=False)
        self.high_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.high_pass(
                1,
                samp_rate,
                200e3,
                400e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_max_xx_0 = blocks.max_ff(4096, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_max_xx_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.blocks_max_xx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.high_pass_filter_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_max_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.high_pass_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "power_indicator")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.variable_function_probe_0-self.offset))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.variable_function_probe_0-self.offset))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.samp_rate, 200e3, 400e3, window.WIN_HAMMING, 6.76))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate*0.45, 1e6, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_bandwidth(self.samp_rate, 0)

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.uhd_usrp_source_0.set_gain(self.rfgain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_sink_x_0.set_frequency_range(self.freq, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_averages(self):
        return self.averages

    def set_averages(self, averages):
        self.averages = averages
        self.blocks_moving_average_xx_1.set_length_and_scale(self.averages, 1/self.averages)




def main(top_block_cls=power_indicator, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

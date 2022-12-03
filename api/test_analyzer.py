#!/usr/bin/python3
# Filename: uplink_latency_analyzer.py
"""
uplink_latency_analyzer.py
An analyzer to monitor uplink packet waiting and processing latency
"""

import matplotlib.pyplot as plt

__all__ = ["TestAnalyzer"]

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from mobile_insight.analyzer.analyzer import *


import time
import dis
import json
from datetime import datetime


# import threading

tbs_table = [
    [16, 32, 56, 88, 120, 152, 208, 256],
    [24, 56, 88, 144, 176, 208, 256, 344],
    [32, 72, 144, 176, 208, 256, 328, 424],
    [40, 104, 176, 208, 256, 328, 440, 568],
    [56, 120, 208, 256, 328, 408, 552, 680],
    [72, 144, 224, 328, 424, 504, 680, 872],
    [88, 176, 256, 392, 504, 600, 808, 1032],
    [104, 224, 328, 472, 584, 680, 968, 1224],
    [120, 256, 392, 536, 680, 808, 1096, 1352],
    [136, 296, 456, 616, 776, 936, 1256, 1544],
    [144, 328, 504, 680, 872, 1032, 1384, 1736],
    [176, 376, 584, 776, 1000, 1192, 1608, 2024],
    [208, 440, 680, 904, 1128, 1352, 1800, 2280],
    [224, 488, 744, 1128, 1256, 1544, 2024, 2536]
]


class TestAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.add_source_callback(self.__msg_callback)

        # Timers 
        self.fn = -1
        self.sfn = -1

        # PHY stats
        self.cum_err_block = {0: 0, 1: 0}  # {0:xx, 1:xx} 0 denotes uplink and 1 denotes downlink
        self.cum_block = {0: 0, 1: 0}  # {0:xx, 1:xx} 0 denotes uplink and 1 denotes downlink

        # MAC buffer
        self.last_buffer = 0
        self.packet_queue = []

        # Stats
        self.all_packets = []
        self.tx_packets = []
        self.tmp_dict = {}

        self.dl_samples = {} # dict of all DL samples
        self.dl_samples_not_found = set([]) # set of DL packet frame nums we haven't found in DCI

        self.found_dl_times = [] # list of timestamps we've found DL packet frame nums
        self.found_dl_time_diffs = [] # list of timedeltas b/t corrdsponding DCI INFO block and DL BLOCK

        self.dls_delayed = [] # list of DL samples that were schedule delayed
        self.dl_match_distance = [] # list of how far frame number of DL block is from the corresponding one listed in DCI Block
        self.dls_repeated_num_times = [] # list of DL samples' Repetition Numbers
        self.dl_data_rates = [] # list of bits transmitted per s
        self.dl_NDIs = [] # list of DL samples' NDI
        self.dl_tansmission_success = [0] # list of DL samples' transmission result

        self.ul_samples = {}
        self.ul_samples_not_found = set([])

        self.found_ul_times = [] # list of timestamps we've found UL packet frame nums
        self.found_ul_time_diffs = [] # list of timedeltas b/t corrdsponding DCI INFO block and UL BLOCK

        self.uls_delayed = [] # list of UL samples that were schedule delayed
        self.ul_match_distance = [] # list of how far frame number of UL block is from the corresponding one listed in DCI Block
        self.uls_repeated_num_times = [] # list of UL samples' Repetition Numbers
        self.ul_data_rates = [] # list of bits transmitted per s
        self.ul_NDIs = [] # list of UL samples' NDI
        self.ul_tansmission_success = [0] # list of UL samples' transmission result

        self.unmatched_DCI = []

        self.all_blocks = []
        
        self.total_FNs = []
        self.total_dl_bits = 0



    def set_source(self, source):
        """
        Set the trace source. Enable the cellular signaling messages

        :param source: the trace source (collector).
        """
        Analyzer.set_source(self, source)
        # source.enable_log_all()
        source.enable_log("LTE_MAC_DL_Transport_Block")
        source.enable_log("LTE_MAC_UL_Transport_Block")
        source.enable_log("LTE_NB1_ML1_GM_DCI_Info")


    def __f_time_diff(self, t1, t2):
        if t1 > t2:
            t_diff = t2 + 10240 - t1
        else:
            t_diff = t2 - t1 + 1
        return t_diff

    def __f_time(self):
        return self.fn * 10 + self.sfn

    def __cmp_queues(self, type, data):
        if type == 1:
            for pkt in self.all_packets:
                if pkt[-2] == data[0]:
                    # print the stats

                    self.all_packets.remove(pkt)
                    return
            self.tx_packets.append(data)
        if type == 2:
            for pkt in self.tx_packets:
                if pkt[0] == data[-2]:
                    # print the stats
                    self.tx_packets.remove(pkt)
                    return
            self.all_packets.append(data)

    def __print_buffer(self):
        pass

    def dl_handler(self, record, frame_num, timestamp):
        if record['RNTI Type'] != 'SI-RNTI':

            end_frame_num = frame_num + 10
            hsfn = record['NPDCCH Timing HSFN']
            ndi = record['NDI']
            if record['Scheduling Delay'] != 0:
                end_frame_num += 10
                self.dls_delayed.append(frame_num)

            for i in range(frame_num, end_frame_num):
                if i in self.dl_samples_not_found:
                    # print(self.dl_samples[i])
                    self.dl_match_distance.append(i - frame_num)

                    self.dl_samples_not_found.remove(i)
                    self.dl_samples[i]['sample']['HSFN'] = hsfn
                    self.dl_samples[i]['sample']['NDI'] = ndi
                    self.all_blocks.append(self.dl_samples[i]['sample'])
                    self.found_dl_times.append(self.dl_samples[i]['time'])
                    self.dls_repeated_num_times.append(record['Repetition Number'])
                    
                    time_diff = timestamp - self.dl_samples[i]['time']
                    self.found_dl_time_diffs.append(round(time_diff.total_seconds() * 1000))
                    
                    if(len(self.dl_NDIs) != 0):
                        res_diff = 1 if self.dl_NDIs[-1] != record['NDI'] else 0
                        self.dl_tansmission_success.append(res_diff)
                    self.dl_NDIs.append(record['NDI'])
                    
                    # find amt of data transmitted per ms at each matched DL's timestamp
                    transmit_time = record['Resource Assignment'] # how long DL transmission will take

                    if transmit_time < 6:
                        transmit_time += 1
                    elif transmit_time == 6:
                        transmit_time = 8
                    else:
                        transmit_time = 10

                    amt_data = tbs_table[record['MCS']][record['Resource Assignment']]
                    amt_data_per_ms = amt_data / transmit_time
                    self.dl_data_rates.append(amt_data_per_ms)

                    for record_buffer in self.unmatched_DCI:
                        if record_buffer['NPDCCH Timing SFN'] * 10 + record_buffer['NPDCCH Timing Sub FN'] == frame_num:
                            self.unmatched_DCI.remove(record_buffer)
                            break

                    return
            record['timestamp'] = timestamp
            self.unmatched_DCI.append(record)

    
    def ul_handler(self, record, frame_num, timestamp):
        if record['RNTI Type'] != 'SI-RNTI':

            end_frame_num = frame_num + 10
            hsfn = record['NPDCCH Timing HSFN']
            ndi = record['NDI']
            if record['Scheduling Delay'] != 0:
                end_frame_num += 10
                self.uls_delayed.append(frame_num)

            for i in range(frame_num, end_frame_num):
                if i in self.ul_samples_not_found:
                    # print('----------------------------------------------------------------')
                    self.ul_match_distance.append(i - frame_num)

                    self.ul_samples_not_found.remove(i)
                    self.ul_samples[i]['sample']['HSFN'] = hsfn
                    self.ul_samples[i]['sample']['NDI'] = ndi
                    self.all_blocks.append(self.ul_samples[i]['sample'])
                    self.found_ul_times.append(self.ul_samples[i]['time'])
                    self.uls_repeated_num_times.append(record['Repetition Number'])
                    
                    time_diff = timestamp - self.ul_samples[i]['time']
                    self.found_ul_time_diffs.append(round(time_diff.total_seconds() * 1000))
                    
                    if(len(self.ul_NDIs) != 0):
                        res_diff = 1 if self.ul_NDIs[-1] != record['NDI'] else 0
                        self.ul_tansmission_success.append(res_diff)
                    self.ul_NDIs.append(record['NDI'])
                    
                    # find amt of data transmitted per ms at each matched UL's timestamp
                    transmit_time = record['Resource Assignment'] # how long UL transmission will take

                    if transmit_time < 6:
                        transmit_time += 1
                    elif transmit_time == 6:
                        transmit_time = 8
                    else:
                        transmit_time = 10

                    amt_data = tbs_table[record['MCS']][record['Resource Assignment']]
                    amt_data_per_ms = amt_data / transmit_time
                    self.ul_data_rates.append(amt_data_per_ms)

                    for record_buffer in self.unmatched_DCI:
                        if record_buffer['NPDCCH Timing SFN'] * 10 + record_buffer['NPDCCH Timing Sub FN'] == frame_num:
                            self.unmatched_DCI.remove(record_buffer)
                            break
                    return
            record['timestamp'] = timestamp
            self.unmatched_DCI.append(record)


    def __msg_callback(self, msg):
    
        if msg.type_id == "LTE_NB1_ML1_GM_DCI_Info":
            decoded_block = msg.data.decode()
            # print('##########################')
            # print('DCI')
            # print(decoded_block,",")
            self.all_blocks.append(decoded_block)
            for record in decoded_block['Records']:
                frame_num = record['NPDCCH Timing SFN'] * 10 + record['NPDCCH Timing Sub FN']
                if record['UL Grant Present'] == 'True':
                    self.ul_handler(record, frame_num, decoded_block['timestamp'])
                    
                else:
                    self.dl_handler(record, frame_num, decoded_block['timestamp'])
            return
    

        if msg.type_id == "LTE_MAC_DL_Transport_Block":
            decoded_block = msg.data.decode()
            # print('##########################')
            # print('DL')
            
            self.save_packet(1, decoded_block)
            return
        
        if msg.type_id == "LTE_MAC_UL_Transport_Block":
            decoded_block = msg.data.decode()
            # print('##########################')
            # print('UL')
            self.save_packet(0, decoded_block)
            return
        
        return

    def save_packet(self, up_or_downlink, decoded_block):
        total_bsr = 0
        for packet in decoded_block['Subpackets']:
            for sample in packet['Samples']:
                SFN = sample['Sub-FN']
                FN = sample['SFN']
                # print('\t' + str(FN * 10 + SFN))

                if up_or_downlink == 0: # uplink
                    bsr_list = []
                    
                    if('Mac Hdr + CE' in sample):
                        for bsr in sample['Mac Hdr + CE']:
                            if bsr['LC ID'] != 'S-BSR': continue
                            total_bsr += bsr['BSR LCG 0']
                            bsr_list.append(bsr['BSR LCG 0'])

                    sample['type_id'] = 'UL Transport Sample'
                    self.ul_samples[FN * 10 + SFN] = {
                        'RNTI Type': sample['RNTI Type'],
                        'time': decoded_block['timestamp'],
                        'bsr_list': bsr_list,
                        'sample': sample
                    }
                    self.ul_samples_not_found.add(FN * 10 + SFN)
                    if len(self.unmatched_DCI) != 0:
                        for record in self.unmatched_DCI:
                            length_unmatch = len(self.unmatched_DCI)
                            if record['UL Grant Present'] == 'True':
                                frame_num = record['NPDCCH Timing SFN'] * 10 + record['NPDCCH Timing Sub FN']
                                self.ul_handler(record, frame_num, record['timestamp'])
                                if length_unmatch != len(self.unmatched_DCI):
                                    break
                else: # downlink
                    sample['type_id'] = 'DL Transport Sample'
                    self.dl_samples[FN * 10 + SFN] = {
                        'RNTI Type': sample['RNTI Type'],
                        'time': decoded_block['timestamp'],
                        'sample': sample
                    }
                    self.dl_samples_not_found.add(FN * 10 + SFN)
                    if len(self.unmatched_DCI) != 0:
                        for record in self.unmatched_DCI:
                            length_unmatch = len(self.unmatched_DCI)
                            if record['DL Grant Present'] == 'True':
                                frame_num = record['NPDCCH Timing SFN'] * 10 + record['NPDCCH Timing Sub FN']
                                self.dl_handler(record, frame_num, record['timestamp'])
                                if length_unmatch != len(self.unmatched_DCI):
                                    break
        
        if(up_or_downlink == 0):
            decoded_block['total_bsr'] = total_bsr
        # print(decoded_block,",")

    def update_time(self, SFN, FN):
        if self.sfn >= 0:      
            self.sfn += 1
            if self.sfn == 10:
                self.sfn = 0
                self.fn += 1
            if self.fn == 1024:
                self.fn = 0
        if SFN < 10:
            self.sfn = SFN
            self.fn = FN

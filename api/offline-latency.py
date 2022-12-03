#!/usr/bin/python
import os
import sys
import shutil
import traceback

import matplotlib.pyplot as plt
import numpy as np

from mobile_insight.monitor import OfflineReplayer
from mobile_insight.analyzer import UplinkLatencyAnalyzer
from test_analyzer import TestAnalyzer

def plot_graph(x, y, x_label, y_label, title):
    if(len(x) != len(y)):
        return
    plt.scatter(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.show()

#Main function 
def uplink_latency_analysis():
    src = OfflineReplayer()
    # src.set_input_path("./logs/latency_sample.mi2log")
    src.set_input_path(sys.argv[1])
    print (sys.argv[1])

    analyzer = TestAnalyzer()
    analyzer.set_source(src)

    src.run()

    return analyzer

def plot_dl(stats):

    num_dl_samples_matched = len(stats.found_dl_time_diffs)
    x_dl = stats.found_dl_times

    print('Matched ' + str(len(x_dl)) + ' DL Samples to DCI Info Blocks')

    plot_graph(x_dl, stats.dl_data_rates, 'DL Sample Timestamps', 'DL Data Rates (bits/ms)', 'DL Data Rates vs DL Sample Timestamps')

    plot_graph(x_dl, stats.dl_match_distance, 'DL Sample Timestamps', 'DL-DCI Match Distances', 'DL-DCI Match Distances vs DL Sample Timestamps')

    plot_graph(x_dl, stats.dls_repeated_num_times, 'DL Sample Timestamps', 'DL Repetition Numbers', 'DL Repetition Numbers vs DL Sample Timestamps')

    plot_graph(x_dl, stats.dl_NDIs, 'DL Sample Timestamps', 'DL NDI', ' DL Sample Timestamps vs DL NDI')

    plot_graph(x_dl, stats.dl_tansmission_success, 'DL Sample Timestamps', 'DL Transmission success', ' DL Sample Timestamps vs DL Transmission success')


    for sample in stats.dl_samples_not_found:
        x_dl.append(stats.dl_samples[sample]['time'])

    y = ([1] * num_dl_samples_matched) + ([0] * len(stats.dl_samples_not_found))

    plot_graph(x_dl, y,'DL Sample Timestamps', 'DCI Info Match Success', 'DCI Info Match Success vs DL Sample Time')    

def plot_ul(stats):

    num_ul_samples_matched = len(stats.found_ul_time_diffs)
    x_ul = stats.found_ul_times

    print('Matched ' + str(len(x_ul)) + ' UL Samples to DCI Info Blocks')

    plot_graph(x_ul, stats.ul_data_rates, 'UL Sample Timestamps', 'UL Data Rates (bits/ms)', 'UL Data Rates vs UL Sample Timestamps')

    plot_graph(x_ul, stats.ul_match_distance, 'UL Sample Timestamps', 'UL-DCI Match Distances', 'UL-DCI Match Distances vs UL Sample Timestamps')

    plot_graph(x_ul, stats.uls_repeated_num_times, 'UL Sample Timestamps', 'UL Repetition Numbers', 'UL Repetition Numbers vs UL Sample Timestamps')

    plot_graph(x_ul, stats.ul_NDIs, 'UL Sample Timestamps', 'UL NDI', ' UL Sample Timestamps vs UL NDI')

    plot_graph(x_ul, stats.ul_tansmission_success, 'UL Sample Timestamps', 'UL Transmission success', ' UL Sample Timestamps vs UL Transmission success')

    for sample in stats.ul_samples_not_found:
        x_ul.append(stats.ul_samples[sample]['time'])

    y = ([1] * num_ul_samples_matched) + ([0] * len(stats.ul_samples_not_found))

    plot_graph(x_ul, y,'UL Sample Timestamps', 'DCI Info Match Success', 'DCI Info Match Success vs UL Sample Time') 

#Program start
stats = uplink_latency_analysis()

#Analysis
if len(sys.argv) > 2 and len(sys.argv) != 6: raise Exception('invalid number of arguments')
userinput = True if len(sys.argv) > 2 else False
FN_low = 0 if len(sys.argv) <= 2 else int(sys.argv[2])
FN_high = 0 if len(sys.argv) <= 2 else int(sys.argv[3])
HSFN_low = 0 if len(sys.argv) <= 2 else int(sys.argv[4])
HSFN_high = 0 if len(sys.argv) <= 2 else int(sys.argv[5])
upperbond = HSFN_high * 1024 + FN_high
lowerbond = HSFN_low * 1024 + FN_low
# print(len(sys.argv), FN_low, FN_high, HSFN_low, HSFN_high)
    
#params
total_dl_bit = 0
total_ul_bit = 0
total_dl_Sub_FN = {}
total_ul_Sub_FN = {}
total_DCI_Sub_FN = {}
ul_NDI = -1
dl_NDI = -1

for packet in stats.all_blocks:
    if packet['type_id'] == 'LTE_NB1_ML1_GM_DCI_Info':
        for record in packet['Records']:
            if record['NPDCCH Timing Sub FN'] in total_DCI_Sub_FN :
                total_DCI_Sub_FN[record['NPDCCH Timing Sub FN']] += 1 
            else:
                total_DCI_Sub_FN[record['NPDCCH Timing Sub FN']] = 1
            
        print(packet,',')
        continue
    if userinput:
        if lowerbond <= packet['HSFN'] * 1024 + packet['SFN']<= upperbond:
            lowerbond = min(lowerbond, packet['HSFN'] * 1024 + packet['SFN'])
            upperbond = max(upperbond, packet['HSFN'] * 1024 + packet['SFN'])
            #downlink
            if packet['type_id'] == 'DL Transport Sample':
                packet['transmission_condition'] = 1 if dl_NDI == -1 else (1 if packet['NDI'] != dl_NDI else 0)
                dl_NDI = packet['NDI']
                total_dl_bit += 8*packet['DL TBS (bytes)']
                if packet['Sub-FN'] in total_dl_Sub_FN :
                    total_dl_Sub_FN[packet['Sub-FN']] += 1 
                else:
                     total_dl_Sub_FN[packet['Sub-FN']] = 1
                print(packet,',')
            #uplink
            if packet['type_id'] == 'UL Transport Sample':
                packet['transmission_condition'] = 1 if ul_NDI == -1 else (1 if packet['NDI'] != ul_NDI else 0)
                ul_NDI = packet['NDI']
                for sample in packet['Mac Hdr + CE'] :
                    total_ul_bit += sample['BSR LCG 0 (bytes)'] if 'BSR LCG 0 (bytes)' in sample else 0
                if packet['Sub-FN'] in total_ul_Sub_FN :
                    total_ul_Sub_FN[packet['Sub-FN']] += 1 
                else:
                     total_ul_Sub_FN[packet['Sub-FN']] = 1
                print(packet,',')
    else:
        lowerbond = min(lowerbond, packet['HSFN'] * 1024 + packet['SFN'])
        upperbond = max(upperbond, packet['HSFN'] * 1024 + packet['SFN'])
        #downlink
        if packet['type_id'] == 'DL Transport Sample':
            packet['transmission_condition'] = 1 if dl_NDI == -1 else (1 if packet['NDI'] != dl_NDI else 0)
            dl_NDI = packet['NDI']
            total_dl_bit += 8*packet['DL TBS (bytes)']
            if packet['Sub-FN'] in total_dl_Sub_FN :
                total_dl_Sub_FN[packet['Sub-FN']] += 1 
            else:
                total_dl_Sub_FN[packet['Sub-FN']] = 1
            print(packet,',')
        #uplink
        if packet['type_id'] == 'UL Transport Sample':
            packet['transmission_condition'] = 1 if ul_NDI == -1 else (1 if packet['NDI'] != ul_NDI else 0)
            ul_NDI = packet['NDI']
            for sample in packet['Mac Hdr + CE'] :
                total_ul_bit += sample['BSR LCG 0 (bytes)'] if 'BSR LCG 0 (bytes)' in sample else 0
            if packet['Sub-FN'] in total_ul_Sub_FN :
                total_ul_Sub_FN[packet['Sub-FN']] += 1 
            else:
                total_ul_Sub_FN[packet['Sub-FN']] = 1
            print(packet,',')

print("total_dl_bit: ", total_dl_bit)
print("Average DL thoughput: ", total_dl_bit/(upperbond - lowerbond))
print("total_ul_bit: ", total_ul_bit)
print("Average UL thoughput: ", total_ul_bit/(upperbond - lowerbond))
print("total_dl_Sub_FN", total_dl_Sub_FN)
print("total_ul_Sub_FN", total_ul_Sub_FN)
print("total_DCI_Sub_FN", total_DCI_Sub_FN)


# plot_dl(stats)
# plot_ul(stats)

total_latency = 0
total_wait = 0
total_trans = 0
total_retx = 0

total_retx = 8 * stats.cum_err_block[0]
for latency in stats.all_packets:
  total_wait += latency['Waiting Latency']
  total_trans += latency['Tx Latency']
  total_retx += latency['Retx Latency']

total_latency = total_wait + total_trans + total_retx
n = len(stats.all_packets)

if (n > 0):
  print ("Average latency is:", float(total_latency) / n)
  print ("Average waiting latency is:", float(total_wait) / n)
  print ("Average tx latency is:", float(total_trans) / n)
  print ("Average retx latency is:", float(total_retx) / n)
else:
  print ("Certain message type(s) missing in the provided log.")
import json
from datetime import datetime

from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def home():
  f = open('boop.json')
  raw_blocks = json.load(f)
  f.close()

  return raw_blocks

airtime = {
  0: 1,
  1: 2,
  2: 3,
  3: 4,
  4: 5,
  5: 6,
  6: 8,
  7: 10
}

@app.route('/blocks')
@cross_origin()
def blocks():

    # Opening JSON file
    f = open('boop.json')
    raw_blocks = json.load(f)
    f.close()

    blocks = get_resource_assignments(raw_blocks)
    return blocks
    '''
    wanna return list of samples and records, where each has the form:
    {
      'type': 'DL-DCI', # one of ['DL-DCI', 'DL-DATA', 'UL-DATA']
      'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 8, 440769),
      'FN': 2,
      'Sub-FN': 2,
      'HSFN': 4,
      'airtime': airtime[resource_assignment]
    }
    '''

    blocks_arr = []

    for block in stuff['found_samples']:
      type_id = 'LTE_MAC_UL_Transport_Block'
      if 'DL TBS (bytes)' in block:
        type_id = 'LTE_MAC_DL_Transport_Block'
      elif 'DCI Repetition Number' in block:
        type_id = 'LTE_NB1_ML1_GM_DCI_Info'
      if type_id == 'LTE_MAC_DL_Transport_Block' or type_id == 'LTE_MAC_UL_Transport_Block':
        blocks_arr.append({
          'type': 'DL-DATA' if type_id == 'LTE_MAC_DL_Transport_Block' else 'UL-DATA',
          'timestamp': block['timestamp'].strftime('%m/%d/%Y %H:%M:%S.%f'),
          'FN': block['SFN'],
          'Sub-FN': block['Sub-FN'],
          'HSFN': block['NPDCCH Timing HSFN'],
          'airtime': airtime[block['Resource Assignment']] # TODO: add Resource Assignment to decoded DL blocks
        })
      else: # LTE_NB1_ML1_GM_DCI_Info
        blocks_arr.append({
          'type': 'DL-DCI',
          'timestamp': block['timestamp'].strftime('%m/%d/%Y %H:%M:%S.%f'),
          'FN': block['NPDCCH Timing SFN'],
          'Sub-FN': block['NPDCCH Timing Sub FN'],
          'HSFN': block['NPDCCH Timing HSFN'],
          'airtime': airtime[block['Resource Assignment']] # TODO: add Resource Assignment to decoded DL blocks
        })

    return blocks_arr

# {
#   'log_msg_len': 40,
#   'type_id': 'LTE_MAC_DL_Transport_Block',
#   'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 9, 241346),
#   'Version': 1,
#   'Num SubPkt': 1,
#   'Subpackets': [
#     {
#       'SubPacket ID': 'DL Transport Block',
#       'Version': 2,
#       'SubPacket Size': 24,
#       'Num Samples': 1,
#       'Samples': [
#         {
#           'Sub-FN': 3,
#           'SFN': 318,
#           'RNTI Type': 'C-RNTI',
#           'HARQ ID': 0,
#           'Area ID': 0,
#           'PMCH ID': 0,
#           'DL TBS (bytes)': 85,
#           'RLC PDUs': 2,
#           'Padding (bytes)': 1,
#           'HDR LEN': 5,
#           'Mac Hdr + CE': [
#             {'Header Field': 35, 'LC ID': '3', 'Len': 2}, {'Header Field': 35, 'LC ID': '3', 'Len': 77}, {'Header Field': 31, 'LC ID': 'Padding', 'Len': -1}]}]}]}


# {'log_msg_len': 32, 'type_id': 'LTE_NB1_ML1_GM_DCI_Info', 'timestamp': 'datetime.datetime(1980, 1, 6, 0, 3, 9, 829344)', 'Version': 3, 'Num of Records': 2, 'Records': [
#   {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 317, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 2, 'Scheduling Delay': 0, 'MCS': 12, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0},
#   {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 320, 'NPDCCH Timing Sub FN': 8, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}]}

def update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, curr_hsfn, curr_fn):
  if greatest_HSFN_and_FN_pair[0] < curr_hsfn:
    greatest = [curr_hsfn, curr_fn]
  elif greatest_HSFN_and_FN_pair[1] < curr_fn:
    greatest = [greatest_HSFN_and_FN_pair[0], curr_fn]
  else:
    greatest = greatest_HSFN_and_FN_pair

  if smallest_HSFN_and_FN_pair[0] > curr_hsfn:
    least = [curr_hsfn, curr_fn]
  elif smallest_HSFN_and_FN_pair[1] > curr_fn:
    least = [smallest_HSFN_and_FN_pair[0], curr_fn]
  else:
    least = smallest_HSFN_and_FN_pair

  return [greatest, least]

def get_resource_assignments(blocks):
  dl_samples_not_found = {}
  ul_samples_not_found = {}
  found_samples = []

  # to figure out size of 2D array
  smallest_HSFN_and_FN_pair = [1024, 1024]
  greatest_HSFN_and_FN_pair = [-1, -1]

  for block in blocks:
    if block['type_id'] == 'LTE_NB1_ML1_GM_DCI_Info':
      for record in block['Records']:
        record['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S.%f') if type(block['timestamp']) == str else block['timestamp']
        frame_num = record['NPDCCH Timing SFN'] * 10 + record['NPDCCH Timing Sub FN']
        if record['RNTI Type'] != 'SI-RNTI':
          end_frame_num = frame_num + 10
          if record['Scheduling Delay'] != 0:
            end_frame_num += 10

          for i in range(frame_num, end_frame_num):
            if record['UL Grant Present'] == 'True':
              if i in ul_samples_not_found:
                # print("UPLINK")
                for ind, lost_sample in enumerate(ul_samples_not_found[i]):
                  if (record['timestamp'] - lost_sample['timestamp']).seconds == 0:
                    # lost_sample['Resource Assignment'] = record['Resource Assignment']
                    lost_sample['airtime'] = airtime[record['Resource Assignment']]
                    lost_sample['HSFN'] = record['NPDCCH Timing HSFN']
                    lost_sample['type'] = 'UL-DATA'
                    found_samples.append(lost_sample)

                    # record['Resource Assignment'] = 0
                    record['airtime'] = 1
                    record['HSFN'] = record['NPDCCH Timing HSFN']
                    record['SFN'] = record['NPDCCH Timing SFN']
                    record['Sub-FN'] = record['NPDCCH Timing Sub FN']
                    record['type'] = 'DL-DCI'
                    found_samples.append(record)

                    greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, record['NPDCCH Timing HSFN'], record['NPDCCH Timing SFN'])
                    greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, record['NPDCCH Timing HSFN'], lost_sample['SFN'])

                    if len(ul_samples_not_found[i]) == 1:
                      del ul_samples_not_found[i]
                    else:
                      del ul_samples_not_found[i][ind]
                    break
                break
            else:
              if i in dl_samples_not_found:
                # print("DOWNLINK")
                for ind, lost_sample in enumerate(dl_samples_not_found[i]):
                  if (record['timestamp'] - lost_sample['timestamp']).seconds == 0:
                    # lost_sample['Resource Assignment'] = record['Resource Assignment']
                    lost_sample['airtime'] = airtime[record['Resource Assignment']]
                    lost_sample['HSFN'] = record['NPDCCH Timing HSFN']
                    lost_sample['type'] = 'DL-DATA'
                    found_samples.append(lost_sample)

                    # record['Resource Assignment'] = 0
                    record['airtime'] = 1
                    record['HSFN'] = record['NPDCCH Timing HSFN']
                    record['SFN'] = record['NPDCCH Timing SFN']
                    record['Sub-FN'] = record['NPDCCH Timing Sub FN']
                    record['type'] = 'DL-DCI'
                    found_samples.append(record)

                    greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, record['NPDCCH Timing HSFN'], record['NPDCCH Timing SFN'])
                    greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, record['NPDCCH Timing HSFN'], lost_sample['SFN'])

                    if len(dl_samples_not_found[i]) == 1:
                      del dl_samples_not_found[i]
                    else:
                      del dl_samples_not_found[i][ind]
                    break
                break
    else: # block['type_id'] == 'LTE_MAC_DL_Transport_Block' or 'LTE_MAC_UL_Transport_Block'
      for packet in block['Subpackets']:
        block['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        for sample in packet['Samples']:
          sample['timestamp'] = block['timestamp']
          SFN = sample['Sub-FN']
          FN = sample['SFN']
          fn = FN * 10 + SFN
          if block['type_id'] == 'LTE_MAC_UL_Transport_Block':
            if fn not in ul_samples_not_found:
              ul_samples_not_found[fn] = [sample]
            else:
              ul_samples_not_found[fn].append(sample)

            # print(ul_samples_not_found.keys())
          else:
            if fn not in dl_samples_not_found:
              dl_samples_not_found[fn] = [sample]
            else:
              dl_samples_not_found[fn].append(sample)

            # print(dl_samples_not_found)

  """
  slap found_samples into 2D array
  rows are for HSFN+FN and columns are for Sub-FN
  """

  # print(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair)

  smallest_idx = smallest_HSFN_and_FN_pair[0] * 1024 + smallest_HSFN_and_FN_pair[1]
  num_rows = (greatest_HSFN_and_FN_pair[0] * 1024 + greatest_HSFN_and_FN_pair[1]) - smallest_idx + 1
  blocks_arr = [[None]*10 for i in range(num_rows)]
  blocks_list = [{
    'SFN': found_samples[0]['SFN'],
    'HSFN': found_samples[0]['HSFN'],
    'blocks': []
  }]

  """
  each entry in blocks_list will correspond to a HSFN and FN key pair and look like
  {
    'SFN': 2,
    'HSFN': 4,
    'blocks': [
      {
        'Sub-FN': 1,
        'airtime': 1,
        'type': 'DL-DCI', # one of ['DL-DCI', 'DL-DATA', 'UL-DATA'],
        ...
      },
      {
        'Sub-FN': 3,
        'airtime': 2,
        'type': 'DL-DCI', # one of ['DL-DCI', 'DL-DATA', 'UL-DATA'],
        ...
      },
      ...
    ]
  }
  """

  def get_key(e):
    return (e['HSFN'] * 1024 + e['SFN']) * 10 + e['Sub-FN']

  found_samples.sort(key=get_key)

  for sample in found_samples:

    # print('x: ', sample['NPDCCH Timing HSFN'] * 1024 + sfn - smallest_idx)
    # print('y: ', sub_fn)

    blocks_arr[sample['HSFN'] * 1024 + sample['SFN'] - smallest_idx][sample['Sub-FN']] = sample

    if blocks_list[-1]['HSFN'] == sample['HSFN'] and blocks_list[-1]['SFN'] == sample['SFN']:
      blocks_list[-1]['blocks'].append(sample)
    else:
      blocks_list.append({
        'SFN': sample['SFN'],
        'HSFN': sample['HSFN'],
        'blocks': [sample]
      })

  return jsonify({
    'blocks_arr': blocks_arr,
    'smallest_idx': smallest_idx,
    'blocks_list': blocks_list
  })

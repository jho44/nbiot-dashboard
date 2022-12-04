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
  f = open('board.json')
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
    f = open('board.json')
    raw_blocks = json.load(f)
    f.close()

    blocks = get_resource_assignments(raw_blocks)
    return blocks

def update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, curr_hsfn, curr_fn):
  if greatest_HSFN_and_FN_pair[0] < curr_hsfn:
    greatest = [curr_hsfn, curr_fn]
  elif greatest_HSFN_and_FN_pair[0] == curr_hsfn and greatest_HSFN_and_FN_pair[1] < curr_fn:
    greatest = [curr_hsfn, curr_fn]
  else:
    greatest = greatest_HSFN_and_FN_pair

  if smallest_HSFN_and_FN_pair[0] > curr_hsfn:
    least = [curr_hsfn, curr_fn]
  elif smallest_HSFN_and_FN_pair[0] == curr_hsfn and smallest_HSFN_and_FN_pair[1] > curr_fn:
    least = [curr_hsfn, curr_fn]
  else:
    least = smallest_HSFN_and_FN_pair

  return [greatest, least]

def get_resource_assignments(blocks):
  dl_samples_not_found = {}
  ul_samples_not_found = {}

  dci_dl_records_not_found = {}
  dci_ul_records_not_found = {}
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
                    record['type'] = 'UL-DCI'

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

          if record['UL Grant Present'] == 'True':
            # means didn't find matching DL TRANSPORT BLOCK to this DCI record
            if frame_num not in dci_ul_records_not_found:
              dci_ul_records_not_found[frame_num] = [record]
            else:
              dci_ul_records_not_found[frame_num].append(record)
          else:
            # means didn't find matching DL TRANSPORT BLOCK to this DCI record
            if frame_num not in dci_dl_records_not_found:
              dci_dl_records_not_found[frame_num] = [record]
            else:
              dci_dl_records_not_found[frame_num].append(record)
    else: # block['type_id'] == 'LTE_MAC_DL_Transport_Block' or 'LTE_MAC_UL_Transport_Block'
      for packet in block['Subpackets']:
        block['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        for sample in packet['Samples']:
          # print('sample: ', sample)
          sample['timestamp'] = block['timestamp']
          SFN = sample['Sub-FN']
          FN = sample['SFN']
          fn = FN * 10 + SFN

          # checking to see whether Transport Block came after corresponding
          # DCI record
          start_fn = fn - 10

          found_prev_dci_record = False

          for i in range(start_fn, fn):
            if block['type_id'] == 'LTE_MAC_UL_Transport_Block':
              if i in dci_ul_records_not_found:
                  # print("UPLINK")
                  for ind, lost_sample in enumerate(dci_ul_records_not_found[i]):
                    if (sample['timestamp'] - lost_sample['timestamp']).seconds == 0:
                      sample['airtime'] = airtime[lost_sample['Resource Assignment']]
                      sample['HSFN'] = lost_sample['NPDCCH Timing HSFN']
                      sample['type'] = 'UL-DATA'
                      found_samples.append(sample)

                      lost_sample['airtime'] = 1
                      lost_sample['HSFN'] = lost_sample['NPDCCH Timing HSFN']
                      lost_sample['SFN'] = lost_sample['NPDCCH Timing SFN']
                      lost_sample['Sub-FN'] = lost_sample['NPDCCH Timing Sub FN']
                      lost_sample['type'] = 'UL-DCI'
                      found_samples.append(lost_sample)

                      greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, lost_sample['NPDCCH Timing HSFN'], lost_sample['NPDCCH Timing SFN'])
                      greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, lost_sample['NPDCCH Timing HSFN'], sample['SFN'])

                      if len(dci_ul_records_not_found[i]) == 1:
                        del dci_ul_records_not_found[i]
                      else:
                        del dci_ul_records_not_found[i][ind]

                      found_prev_dci_record = True
                      break
                  if found_prev_dci_record:
                    continue
            else:
              if i in dci_dl_records_not_found:
                  # print("DOWNLINK")
                  for ind, lost_sample in enumerate(dci_dl_records_not_found[i]):
                    if (sample['timestamp'] - lost_sample['timestamp']).seconds == 0:
                      sample['airtime'] = airtime[lost_sample['Resource Assignment']]
                      sample['HSFN'] = lost_sample['NPDCCH Timing HSFN']
                      sample['type'] = 'DL-DATA'
                      found_samples.append(sample)

                      lost_sample['airtime'] = 1
                      lost_sample['HSFN'] = lost_sample['NPDCCH Timing HSFN']
                      lost_sample['SFN'] = lost_sample['NPDCCH Timing SFN']
                      lost_sample['Sub-FN'] = lost_sample['NPDCCH Timing Sub FN']
                      lost_sample['type'] = 'DL-DCI'
                      found_samples.append(lost_sample)

                      greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, lost_sample['NPDCCH Timing HSFN'], lost_sample['NPDCCH Timing SFN'])
                      greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair = update_HSFN_and_FN_extremes(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair, lost_sample['NPDCCH Timing HSFN'], sample['SFN'])

                      if len(dci_dl_records_not_found[i]) == 1:
                        del dci_dl_records_not_found[i]
                      else:
                        del dci_dl_records_not_found[i][ind]
                      found_prev_dci_record = True
                      break
                  if found_prev_dci_record:
                    continue

          if block['type_id'] == 'LTE_MAC_UL_Transport_Block':
            if fn not in ul_samples_not_found:
              ul_samples_not_found[fn] = [sample]
            else:
              ul_samples_not_found[fn].append(sample)

            # print(ul_samples_not_found.keys())
          else: # LTE_MAC_DL_TRANSPORT_Block
            if fn not in dl_samples_not_found:
              dl_samples_not_found[fn] = [sample]
            else:
              dl_samples_not_found[fn].append(sample)

            # print(dl_samples_not_found)

  """
  slap found_samples into 2D array
  rows are for HSFN+FN and columns are for Sub-FN
  """

  print(greatest_HSFN_and_FN_pair, smallest_HSFN_and_FN_pair)

  smallest_idx = smallest_HSFN_and_FN_pair[0] * 1024 + smallest_HSFN_and_FN_pair[1]
  num_rows = (greatest_HSFN_and_FN_pair[0] * 1024 + greatest_HSFN_and_FN_pair[1]) - smallest_idx + 2
  # add 1 for greatest - smallest and add another 1 since HSFN and FN's smallest value is 1
  # while lists index by 0

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

  # states for figuring out transmission success of each data unit
  last_dl_NDI = -1
  last_ul_NDI = -1
  last_dl_inds = {}
  last_ul_inds = {}

  for ind, sample in enumerate(found_samples):
    # print(sample['type'], sample['HSFN'], sample['SFN'])

    # print('x: ', sample['NPDCCH Timing HSFN'] * 1024 + sfn - smallest_idx)
    # print('y: ', sub_fn)

    # add transmission success data now that everything's sorted
    if sample['type'] == 'UL-DCI':
      if last_ul_NDI != -1 and 'blocks_arr_inds' in last_ul_inds: # if this isn't the first one we've found (which we can't have previous NDI info about)
        NDI_diff = (1 if sample['NDI'] != last_ul_NDI else 0)
        blocks_arr[last_ul_inds['blocks_arr_inds'][0]][last_ul_inds['blocks_arr_inds'][1]]['tx-success'] = NDI_diff # set the tx_success of the previous UL sample

      last_ul_NDI = sample['NDI']
      sample['type'] = 'DL-DCI' # set back to DL-DCI since all DCIs are technically all DL packets
    elif sample['type'] == 'DL-DCI':
      if last_dl_NDI != -1 and 'blocks_arr_inds' in last_dl_inds: # if this isn't the first one we've found (which we can't have previous NDI info about)
        NDI_diff = (1 if sample['NDI'] != last_dl_NDI else 0)
        blocks_arr[last_dl_inds['blocks_arr_inds'][0]][last_dl_inds['blocks_arr_inds'][1]]['tx-success'] = NDI_diff # set the tx_success of the previous UL sample

      last_dl_NDI = sample['NDI']

    if sample['type'] == 'UL-DATA':
      last_ul_inds['blocks_list_ind'] = len(blocks_list) - 1
    elif sample['type'] == 'DL-DATA':
      last_dl_inds['blocks_list_ind'] = len(blocks_list) - 1

    row = sample['HSFN'] * 1024 + sample['SFN'] - smallest_idx
    col = sample['Sub-FN']
    blocks_arr[row][col] = sample
    if sample['type'] == 'UL-DATA':
      last_ul_inds['blocks_arr_inds'] = (row, col)
    elif sample['type'] == 'DL-DATA':
      last_dl_inds['blocks_arr_inds'] = (row, col)

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
    'blocks_list': blocks_list,
    'greatest_HSFN_and_FN_pair': greatest_HSFN_and_FN_pair,
    'smallest_HSFN_and_FN_pair': smallest_HSFN_and_FN_pair
  })

import os
import wave
import contextlib

def get_duration(filepath):

    with contextlib.closing(wave.open(filepath,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


datapath = '/Users/royal/Desktop/audio_data/TIMIT/DENOISED/'

filenames = os.listdir(datapath)


usrs_set = set()

for filename in filenames:
    usr = filename.split('_')[0]
    usrs_set.add(usr)

usrs_list = list(usrs_set)

train_list = usrs_list[:530]
test_list = usrs_list[530:]

train_set = set(train_list)
test_set = set(test_list)

f_train_mtdm = open('/Users/royal/Desktop/pyannote-db-timit/Timit/data/TimitSpeakerVerificationProtocol.train.mdtm', 'w')
f_val_mtdm = open('/Users/royal/Desktop/pyannote-db-timit/Timit/data/TimitSpeakerVerificationProtocol.val.mdtm', 'w')
f_test_mtdm = open('/Users/royal/Desktop/pyannote-db-timit/Timit/data/TimitSpeakerVerificationProtocol.test.mdtm', 'w')


train_ctr, val_ctr, test_ctr = 0, 0, 0

usr_str = {}

for filename in filenames:
    usr = filename.split('_')[0]
    dur = get_duration(datapath+filename)
    mdtm_line = '{} 1 0.0 {} {} {} {} {}\n'.format(filename.split('.')[0], str(dur), 'speaker',
                                                 'NA', 'unknown', usr )

    if usr not in usr_str:
        usr_str[usr] = []

    usr_str[usr].append(mdtm_line)


for usr in usr_str:
    lines = usr_str[usr]

    if usr in test_set:
        for line in lines:
            test_ctr += 1
            f_test_mtdm.write(line)

    else:
        train_portion = int(0.8*len(lines))
        train_lines = lines[:train_portion]
        val_lines = lines[train_portion:]

        for line in train_lines:
            train_ctr += 1
            f_train_mtdm.write(line)

        for line in val_lines:
            val_ctr += 1
            f_val_mtdm.write(line)


print('TRAIN : {} VAL : {} TEST : {}'.format(train_ctr, val_ctr, test_ctr))
f_train_mtdm.close()
f_val_mtdm.close()
f_test_mtdm.close()



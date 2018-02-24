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

train_list = usrs_list[:450]
val_list = usrs_list[450:530]
test_list = usrs_list[:450]

train_set = set(train_list)
val_set = set(val_list)
test_set = set(test_list)

f_train_mtdm = open('/Users/royal/Desktop/pyannote-db-template/Timit/data/TimitSpeakerVerificationProtocol.train.mdtm', 'w')
f_val_mtdm = open('/Users/royal/Desktop/pyannote-db-template/Timit/data/TimitSpeakerVerificationProtocol.val.mdtm', 'w')
f_test_mtdm = open('/Users/royal/Desktop/pyannote-db-template/Timit/data/TimitSpeakerVerificationProtocol.test.mdtm', 'w')


train_ctr, val_ctr, test_ctr = 0, 0, 0
for filename in filenames:
    usr = filename.split('_')[0]
    dur = get_duration(datapath+filename)
    mdtm_line = '{} 1 0.0 {} {} {} {} {}\n'.format(filename.split('.')[0], str(dur), 'speaker',
                                                 'NA', 'unknown', usr )

    if usr in train_set:
        train_ctr += 1
        f_train_mtdm.write(mdtm_line)
    elif usr in val_set:
        val_ctr += 1
        f_val_mtdm.write(mdtm_line)
    else:
        test_ctr += 1
        f_test_mtdm.write(mdtm_line)


print('TRAIN : {} VAL : {} TEST : {}'.format(train_ctr, val_ctr, test_ctr))
f_train_mtdm.close()
f_val_mtdm.close()
f_test_mtdm.close()



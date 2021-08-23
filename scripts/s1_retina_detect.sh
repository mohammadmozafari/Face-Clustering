python_file='./src/s1_retina_detect.py'

network='mobile0.25'
trained_model='./trained_models/mobilenet0.25_Final.pth'
device='gpu'

python $python_file --network $network --trained_model $trained_model --device $device
python_file='./src/evaluate_threshold_clustering.py'

input_file1='./data/IJB-B/512.fea.npy'
labels1='./data/IJB-B/512.labels.npy'

input_file2='./data/features/features_1_9_.npy'
labels2='./data/labels/labels.npy'

python $python_file $input_file1 --labels_path $labels1
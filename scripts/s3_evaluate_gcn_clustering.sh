python_file='./src/s3_evaluate_gcn_clustering.py'

input_file='./data/program_data/features_1_30_.npy'
labels='./data/IJB-B/512.labels.npy'
no_labels='nothing'

knn_graph1='./data/IJB-B/knn.graph.512.bf.npy'
knn_graph2='./data/program_data/knn_bt.npy'

model_path='./trained_models/gcn.ckpt'

python $python_file --val_feat_path $input_file --val_knn_graph $knn_graph2 --val_label_path $no_labels --checkpoint $model_path
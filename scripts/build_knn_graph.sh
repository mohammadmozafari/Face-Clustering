python_file='./src/build_knn_graph.py'

feat_path1='./data/my-family/features_1_9_.npy'
feat_path2='./data/IJB-B/512.fea.npy'

k1=2
k2=200

alg1='brute'
alg2='kd_tree'
alg3='ball_tree'

out_path1='./data/my-family/knn_graph.npy'
out_path2='./data/IJB-B/knn_bf.npy'
out_path3='./data/IJB-B/knn_kd.npy'
out_path4='./data/IJB-B/knn_bt.npy'

python $python_file --feat_path $feat_path2 --k $k2 --alg $alg3 --out_path $out_path4 
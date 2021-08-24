python_file='./src/s2_evaluate_lfw_features.py'

images='./data/lfw-results/paths_1_13233_.csv'
pairs_path='./data/lfw-results/pairs.txt'
features='./data/lfw-results/features_1_13233_.npy'

python $python_file --images $images --pairs_path $pairs_path --features $features
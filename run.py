#!/usr/bin/env python3
# coding: utf-8

import os
import argparse
import numpy as np
import tensorflow as tf
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import metrics
os.chdir('dir')

def startup(test_data,test_label, score_rnn, label_rnn):
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:    
        model_file=tf.train.latest_checkpoint('ckpt/')
        new_saver = tf.train.import_meta_graph('train.ckpt-275.meta')
        new_saver.restore(sess,model_file)

        pred = tf.get_collection('network-output')[0]

        graph = tf.get_default_graph()
        x = graph.get_operation_by_name('x').outputs[0]
        y = graph.get_operation_by_name('y').outputs[0]

        X_test=np.loadtxt(open(test_data,"rb"),delimiter=",",skiprows=0)
        y_test=np.loadtxt(open(test_label,"rb"),delimiter=",",skiprows=0)
        X_test = np.expand_dims(X_test,2)

        y_score=sess.run(pred,feed_dict={x:X_test, seqlen: test_seqlen})
        metrics.roc_auc_score(np.array(y_test).ravel(), np.array(y_score).ravel(), average='micro')
        fpr, tpr, thresholds = metrics.roc_curve(np.array(y_test).ravel(),np.array(y_score).ravel())
        auc = metrics.auc(fpr, tpr)

        a=np.array(y_score).ravel()
        b=np.array(y_test).ravel()
        np.savetxt(score_rnn,a, delimiter = ',')
        np.savetxt(label_rnn,b, delimiter = ',')
        print("Test Finished!")
        print("AUC=:",auc)

        plt.plot(fpr, tpr, color='darkorange',lw=2, label='ROC curve (area = %0.2f)' % auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
        print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: X_test, y: y_test}))
        print("Test Finished!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testdata',  nargs='?', default='test_data.csv',  type=str)
    parser.add_argument('--testlabel', nargs='?', default='test_label.csv', type=str)
    parser.add_argument('--scorernn',  nargs='?', default='score_rnn.csv',  type=str)
    parser.add_argument('--labelrnn',  nargs='?', default='label_rnn.csv',  type=str)
    args = parser.parse_args()
    startup(args.testdata, args.testlabel, args.scorernn, args.labelrnn)
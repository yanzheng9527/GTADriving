#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import matplotlib.pyplot as plt

from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint

from model import MANet

def acceptSample(sample):
	throttle = sample[1][4]
	steering = sample[1][3]

	if (np.absolute(steering) > 0.025 and throttle > 0.15):
		return True
	
	if(throttle < 0.15 or np.absolute(steering) < 0.025):
		if(np.random.rand() > 0.95):
			return True

	return False

if __name__ == '__main__':

	datasetFiles = ['/Users/yanzheng/Downloads/GTAVDataset2/dataset.txt']
	
	Net = MANet()

	dataset = Net.toSequenceDataset(datasetFiles)	
	dataset = [sample for sample in dataset if acceptSample(sample)]
	
	valLen = int(len(dataset)*0.1)
	valDataset = dataset[0:valLen]
	dataset = np.delete(dataset, np.s_[0:valLen], 0)

	trainGenerator = Net.dataGenerator(dataset)
	valGenerator = Net.dataGenerator(valDataset)

	model = Net.getModel()
	model.compile(optimizer=RMSprop(), loss='mse', clipnorm=1.0)
	ckp_callback = ModelCheckpoint("model.h5", monitor="val_loss", save_best_only=True, save_weights_only=True, mode='min')
	
	model.fit_generator(
		trainGenerator,
		samples_per_epoch=len(dataset),
		nb_epoch=1000,
		validation_data=valGenerator,
		nb_val_samples=len(valDataset),
		callbacks=[ckp_callback]
	)

# pylint: skip-file
import os
from collections import Counter
import string
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np

# edits
# changed float32 to float due to pylint error

class Dataset:
    def __init__(self, img_height, img_width, batch_size, output, num_output):
        self.img_height = img_height
        self.img_width = img_width
        self.batch_size = batch_size
        self.output = output
        self.num_output = num_output
        self.num_classes = len(output)
        
        print("Image Height: " + str(self.img_height))
        print("Image Width: " + str(self.img_width))
        print("Batch Size: " + str(self.batch_size))
        print("Number of Output Classes: " + str(self.num_classes))
        
        self.imgs_gray = []
        self.imgs_rgb = []
        self.labels = []
        self.encoded_labels = []
        self.encoded_label_strings = []
        self.n = 0
        self.current_index = 0
        return
     
    def build_data_from_file(self, file, relative_path, segment):
        imgs_gray = []
        imgs_rgb = []
        labels = []
        encoded_labels = []
        encoded_label_strings = []
        n = 0
        
        with open(relative_path + file, 'r') as fp:
            for line in fp:
                self.n = self.n + 1
                filename = line.split(' ')[0]
                filename = relative_path + filename
                gray, rgb, img = self.get_img(filename)
                if gray is None:
                    continue
                
                parsed_filename = filename.split("_") # filename is in format number_label_number
                label = parsed_filename[2]
                encoded_label, encoded_label_string = self.encode_label(label, self.num_output)
                
#                self.print_sample(filename, label, encoded_label, encoded_label_string, rgb, gray, img)

                # store data
                imgs_gray.append(gray)
                imgs_rgb.append(rgb)
                labels.append(label)
                encoded_labels.append(encoded_label)
                encoded_label_strings.append(encoded_label_string)
            
            self.n = self.n + n
            self.indexes = list(range(self.n))
            self.imgs_gray = imgs_gray
            self.imgs_rgb = imgs_rgb
            self.labels = np.asarray(labels, dtype=object)
            self.encoded_labels = np.asarray(encoded_labels)
            self.encoded_label_strings = np.asarray(encoded_label_strings).reshape(self.n, 1)
            return
        
#    def build_data_from_directory(self, directory):
#        imgs_gray = []
#        imgs_rgb = []
#        labels = []
#        encoded_labels = []
#        encoded_label_strings = []
#        
#        for filename in os.listdir(self.directory):
#            filepath = self.directory + filename
#            gray, rgb = self.get_img(filepath)
#            if gray is None:
#                continue
#                
#            parsed_filename = filename.split("_") # filename is in format number_label_number
#            label = parsed_filename[1]
#            encoded_label = np.asarray(list(map(lambda x: letters.index(x), label)))
#            encoded_label = np.pad(encoded_label, (0, 32 - len(encoded_label)%32), mode='constant')
#            encoded_label = encoded_label.astype(np.int32)
#            encoded_label_string = ' '.join(str(x) for x in encoded_label.tolist())
#            
#            # print data
#            print("Filepath: " + filepath)
#            print("Label: " + label + " | Encoded Label: " + str(encoded_label))
#            print("Encoded Label String: " + encoded_label_string)
#            plt.imshow(img)
#            plt.show()
#
#            # store data
#            imgs_gray.append(gray)
#            imgs_rgb.append(rgb)
#            labels.append(label)
#            encoded_labels.append(encoded_label)
#            encoded_label_strings.append(encoded_label_string)
#          
#        self.imgs_gray = imgs_gray
#        self.imgs_rgb = imgs_rgb
#        self.labels = np.asarray(labels, dtype=object)
#        self.encoded_labels = np.asarray(encoded_labels)
#        self.encoded_label_strings = np.asarray(encoded_label_strings).reshape(self.n, 1)
#        return
    
    def get_img(self, file):
#        print(file)
        img = cv2.imread(file)
        if img is None:
            print("Image at " + file + " cannot be opened")
            return None, None
        
        # print("Image Shape Before Resize: " + str(img.shape))
        img_resize = cv2.resize(img, (self.img_width, self.img_height), interpolation = cv2.INTER_AREA)
        # print("Image Shape After Resize: " + str(img_resize.shape))
        
        # grayscale image is the input into network
        gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
        gray = gray.astype(np.float32)
        gray /= 255
        return gray, rgb, img
    
    def encode_label(self, label, length):
        # all labels need to be unifrom length
        # append empty space to labels 
        filler_length = length - len(label)%32
        filler = " " * filler_length
        label = label + filler
      
        encoded_label = np.asarray(list(map(lambda x: self.output.index(x), label)))
        encoded_label = encoded_label.astype(np.int32)
        encoded_label_string = ' '.join(str(x) for x in encoded_label.tolist())
        return encoded_label, encoded_label_string
    
    def print_sample(self, filename, label, encoded_label, encoded_label_string, rgb, gray, img):
        # print data
        print("Filepath: " + filename)
        print("Label: " + label + " | Encoded Label: " + str(encoded_label))
        print("Encoded Label String: " + encoded_label_string)
        
        print("Original:")
        plt.imshow(img)
        plt.axis("off")
        plt.show()                          
        
        print("Grayscale:")
        plt.imshow(gray, cmap='gray')
        plt.axis("off")
        plt.show()
        return

    def get_output_size(self):
        return self.num_output
    
    def next_sample(self):
        self.current_index = self.current_index + 1
        if self.current_index >= self.n:
            print("Shuffle Indexes")
            self.current_index = 0
            random.shuffle(self.indexes)
            
        sample_index = self.indexes[self.current_index]
        #print("Current Index: " + str(self.current_index) + " Sample Index: " + str(sample_index))
        return self.imgs_gray[sample_index], self.imgs_rgb[sample_index], self.encoded_labels[sample_index]
    
    def next_batch(self):
        #print("# of Samples: " + str(self.n))
        X = []
        Y = []
        imgs_rgb= []
        for i in range(self.batch_size):
            x, rgb, y = self.next_sample()
            shape = x.shape
            x = np.reshape(x, (shape[0], shape[1], 1))
            X.append(x)
            Y.append(y)
        X = np.asarray(X, dtype=np.float32)
        imgs_rgb = np.asarray(imgs_rgb, dtype=np.float32)
        Y = np.asarray(Y)
        print("Batch images shape: " + str(X.shape))
        print("Batch labels shape: " + str(Y.shape))
        return X, imgs_rgb, Y
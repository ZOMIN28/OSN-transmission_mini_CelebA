# OSN-transmission_mini_CelebA

#### The OSN-transmission Mini CelebA Dataset in "DF-RAP: A Robust Adversarial Perturbation for Defending against Deepfakes in Real-world Social Network Scenarios"

### 1. Introduction

This is the paper “DF-RAP: A Robust Adversarial Perturbation for Defending against Deepfakes in Real-world Social Network Scenarios" OSN-transmission CelebA sampling dataset collected by manual upload and download. This dataset includes 30,000 facial images of size $256\times256$ transmitted through online social networks (OSN) and their corresponding original images. Among them, Facebook, Twitter, WeChat and Weibo were selected as the transmission OSN, with 7500 images each.

**Dataset link:**    
Google Drive :  https://drive.google.com/file/d/1Bb6o6wQ8qTrxDN6NJUeoeUVq02Btjg-y/view?usp=drive_link


### 2. Investigation on the lossy operating mechanism of OSNs

We conducted an in-depth investigation of the 4 compression and resize mechanisms used by OSN.

#### 2.1. Compression

The image compression quality factor (QF) is adaptively determined based on the size and content of the image. As shown in Fig. 1 (a), JPEG compression with QF values ranging from 71 to 95 is used by Facebook, with QF=92 being the most commonly used. Our investigation also revealed that Facebook tends to conduct compression with lower QFs (e.g., QF=71) for small-sized but content-rich images. Twitter employs a simpler compression strategy: larger images are compressed using JPEG with QF=85, while smaller images are not compressed. According to the results presented in Fig.2 (b), this threshold is reported as $900\times900$. For WeChat and Weibo, more complex and stringent lossy operations are employed, making quantification difficult. In addition, we explored the average changes in pixel values for images of different sizes. As shown in Fig. 2 (b), WeChat produces the most significant changes to the image. These findings highlight the disparity in the distribution of real compressed images across different OSN platforms, confirming the complexity of the lossy compression mechanism employed by OSNs.

<img src="images\fig1.png" alt="fig1" style="zoom:67%;" />

For Weibo, there is a big difference between using the IOS terminal and the PC web terminal to transmit images. iPhone uses a new image format to save pictures on Weibo, namely `.HEIF`. Compared to `.jpg`, `.HEIF` implements more severe compression, saving and transmitting data more efficiently while maintaining good visual quality. On the PC web page, Weibo will only perform very slight compression on images, or even no compression at all. It is worth noting that in this work, **we used iPhone to upload and download images on Weibo.**

#### 2.2. Resize

Additionally, we studied the resizing strategy of OSNs. The specific resizing details for the different social media platforms are displayed in Table 1. Notably, to the best of our knowledge, WeChat and Weibo only constrain the width of the image, while there is no upper bound on the length of the image within the knowable range. Moreover, Twitter is reported to have a larger threshold for performing resizing. In this paper, we focus on adversarial perturbations aimed at resisting OSN compression, considering that compression operations are more destructive and widespread. 

<img src="images\tab1.png" alt="tab1" style="zoom:67%;" />

**Please note:** As most social platforms, their compression policies may be adjusted and updated frequently to adapt to changing network environments, user needs, and technological developments. These platforms may make adjustments based on user feedback, technological advancements, and competitor strategies to ensure that their compression strategies maximize performance and efficiency while maintaining image and video quality. For example, Weibo sometimes chooses `2000px` as the threshold for implementing Resize. **Therefore, the survey data provided in this work are for reference only.**



### 3. Collection Details

The compression mechanism adopted by a certain OSN is closely related to the size of the image. Therefore, uploading only the $256\times256$ resolution image contained in CelebA cannot obtain sufficient OSN compression information. Therefore, at the stage of uploading images to OSNs, to simulate photo sharing in real-world scenarios, a crude but effective approach was taken: we stitch images randomly to obtain examples of different sizes to upload. For Twitter, the maximum size of the stitched image is limited to ,$4096\times4096$ while it is limited to $1280\times2048$ for others.      

We used a `Legion Y9000K2021H` running the Windows 11 operating system to upload and download images on Facebook and Twitter, and an `iPhone 13` with IOS 16.6 to accomplish this task on WeChat and Weibo.



### 4. Why Are Compressed Images in `.png` Format?

As mentioned above, we randomly stitch images and upload them to OSNs and download them. After that, we will crop the downloaded large stitched image in `.jpg` format to obtain a batch of cropped small images corresponding to the original images with a size of $256\times256$. In order to fully retain the lossy compression information of the cropped images and prevent the destruction of this information by secondary compression, we save them in lossless `.png` format.



### 5. How to Use It?

We provide a python script `data_loader.py` for reading these OSN transmitted images and their corresponding original images in pairs.
```
    celeba_loader = get_loader("OSN-transmission_mini_CelebA/original_images/","OSN-transmission_mini_CelebA/transmission_images/","OSN-transmission_mini_CelebA/attributes.txt")
    for n,(o_img,c_img,c_org) in enumerate(tqdm(celeba_loader)):
        ······
```


### 6. Reference

```
@article{qu2024df,
  title={DF-RAP: A Robust Adversarial Perturbation for Defending against Deepfakes in Real-world Social Network Scenarios},
  author={Qu, Zuomin and Xi, Zuping and Lu, Wei and Luo, Xiangyang and Wang, Qian and Li, Bin},
  journal={IEEE Transactions on Information Forensics and Security},
  year={2024},
  publisher={IEEE}
}
```


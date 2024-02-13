# Fovea-localization-by-blood-vessel-vector
  We used four datasets: DRIVE,MESSIDOR,Kaggle, and IDRID.DRIVE was used to train and detect blood vessels, while kaggle and messidor were used to locate the fovea and evaluate the proposed model.


  
  The program in OD-UNET-MASTER uses u-net for rough segmentation of OD, similarly, Vesselsegmentation uses u-net for blood vessel segmentation.


  
  FindOD is a program to obtain the final segmentation result of the video disc after coarse segmentation with u-net through the probabilistic bubble model.vessel aid is a program to obtain the final blood vessel results through the probabilistic bubble model after the blood vessels are roughly segmented with u-net.



  vesselvector uses the BVV model for final foveal positioning.

  
  
  

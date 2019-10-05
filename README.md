## `youtubewatcher`

A python script that detects movement/frame difference in an otherwise still video (like on youtube)

## Why? 
So I can idle and look for pokemon in the Galar Live Footage video event here: https://www.youtube.com/watch?v=Ya3CyVN5S_w

## What?
Runs on `python 2.7.x`.

Requires `cv2`, `numpy`, and `mss`.

Install packages individually using `pip install [packagename]`.
OpenCV (cv2) is a bit trickier, google it and good luck!

## How?
Clone the repo.

Create a `found` folder under src and then a `HD` folder inside found.

Open the stream on an empty part of your desktop.

Edit `src` line 17 to put the video inside the capture box.

Tweak the values on lines 20 to 24 as needed.

If something moves (or differs) from the first frame of the video feed then it should be detected.

If something is detected in the frame then that frame is saved in `found/HD`.

## Results ?
With a little tweaking it can find movement and track it pretty well as long as the background doesnt change too much. Here are some of the Pokemon I found during the Galar Streaming event. 
![](https://i.imgur.com/9R9Prx7.png)
![](https://i.imgur.com/7CJCuR9.png)

I then stitched subsequent images together into a gif using Imageflip, note: the script as is itself only outputs still images.
![](results/3cg5h9.gif)
![](results/3cg6oe.gif)
![](results/3cggig.gif)
![](results/3cggn5.gif)

## Wow! How do I give you a pat on the back?
♥ Star my repo. 

♥♥ Gift me gold [on reddit](https://www.reddit.com/user/thelunararmy). (or upvote my stuff if you broke)

♥♥♥♥♥ Send me [caffeine money](https://www.paypal.com/paypalme2/tlafreelance)

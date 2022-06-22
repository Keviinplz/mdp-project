# MDP Project (r/place)

This project has been created to detect the use of bots in `r/place` activity from Reddit as final project to Masive Data Processing course.

Members:

- Nicolas Olguin
- Juan Quilapi
- Kevin Pinochet

# Preamble

[r/place](https://www.reddit.com/r/place/) is an activity that takes place on Reddit, which consists of a canvas of (m, n) pixels where users can color a pixel every 5 minutes (if they are registered on Reddit) or every 20 minutes. This activity was first performed in 2017 in honor of April Fool's Day.

The last one was held in 2022, and the moderator in charge provided data about the activity. Using this data we are looking to detect the use of bots in the activity.

# Data Source

The data is available as a CSV file with the following format:

`timestamp, user_id, pixel_color, coordinate`

Where: 
-   Timestamp: the UTC time of the tile placement

-   User_id: a hashed identifier for each user placing the tile. These are not reddit user_ids, but instead a hashed identifier to allow correlating tiles placed by the same user.

-   Pixel_color: the hex color code of the tile placedCoordinate - the “x,y” coordinate of the tile placement. 0,0 is the top left corner. 1999,0 is the top right corner. 0,1999 is the bottom left corner of the fully expanded canvas. 1999,1999 is the bottom right corner of the fully expanded canvas.

Example row (the first recorded placement on the position 0,0.):

`2022-04-03 17:38:22.252 UTC,yTrYCd4LUpBn4rIyNXkkW2+Fac5cQHK2lsDpNghkq0oPu9o//8oPZPlLM4CXQeEIId7l011MbHcAaLyqfhSRoA==,#FF3881,"0,0"`

Inside the dataset there are instances of moderators using a rectangle drawing tool to handle inappropriate content. These rows differ in the coordinate tuple which contain four values instead of two–“x1,y1,x2,y2” corresponding to the upper left x1, y1 coordinate and the lower right x2, y2 coordinate of the moderation rect. These events apply the specified color to all tiles within those two points, inclusive.

The link of the entire dataset is available [here](https://placedata.reddit.com/data/canvas-history/2022_place_canvas_history.csv.gzip). 

However, we actually used a simplified dataset with timestamp and users as integers (so size drops to `5.2 gb`)

Where:
* time: milliseconds since first placement. First placement was 2022-04-01 12:44:10.315

* user_id: id of users, starts at 0. The original file had hashed strings, but since we don't know the hashing algorithm, it can be replaced with simple id counting (256 bits to 64 bits).

* x: the x coordinate of the pixel in the canvas

* y: the y coordinate of the pixel in the canvas

* color: value between 0 - 31. see color index table below for corresponding real color.

* mod: 1 if it's a part of one of the placed rectangles by moderators, 0 if not. (we filter all files with mod equals to 1)

Link is available [here](https://drive.google.com/file/d/1WYuZaoQxBszO_3mNrD4rQlCS5aiKPFvk/view?usp=sharing)

# How to development

This repository use `poetry` as package manager, [you have to install it first](https://python-poetry.org/docs/master/#installing-with-the-official-installer).

If you already have `poetry` installed, you can run `poetry install` to install all dependencies.

# Folder Structure

The repository has the following folder structure:

```
├── data             <--- Data that will use to make predictions, DO NOT UPLOAD TO GITHUB
│   ├── production
│   └── testing
├── src              <--- source code for map-reduce framework
│   ├── mappers
│   └── reducers
├── tests            <--- code testing (yes, we tested all because we are excelents software engineers :D).
├── output           <--- Files ready-to-use for hadoop streams.
├── main.py          <--- main file for map-reduce framework, with --mapper and --reducer flags to specify which mapper and reducer to use
└── main.ipynb       <--- jupyter notebook to interact with data.
```

Enjoy!
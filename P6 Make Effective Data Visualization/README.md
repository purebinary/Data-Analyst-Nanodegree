# P6: Make Effective Data Visualization

## Summary 

I use the Prosper Loan data to create a line chart, which shows Borrower Rate by six income ranges categories, from "Not employed" to "100,000+". Since Prosper didn't have IncomeRange category before Q1 2007, so I chose data from Q1 2007. The main purpose is to find who received the lowest borrower rate. Each category line can be chose by mouse over, click. Tool-tip for each line or each cycle will be rendered when hover it. A table includes all six categories can be clicked to select lines too.

## Design 
My first version of visualization was more concerned on the exploratory of variables of loan amount, payment & interest, borrower rate and income etc. based on the yearly average, so I use line chart to tender those variables trends with author-driven and viewer-driven ideas. This is the first time I use D3 to implement visualization. At the project beginning, I focused more on d3 coding technology, didn't consider the explanatory data carefully ([First plot][1]). 
   [1]: http://bl.ocks.org/purebinary/raw/9833242f34eb015caa33541ad1fe73a5/

After posting my visualization and getting feedbacks, I realized that it more like exploratory and didn't have a clear finding on my first visualization. Then, I loaded the raw data into R, explored the variables, and found out that income correlated with borrower rate, credit rating, debt ratio etc. Therefore, I decided to keep line chart design style to show the borrower rate trends quarterly for all income categories. The main outcome is that the more income borrowers have, the less borrower rate is applied to them, borrowers with income above $100,000 received the lowest borrower rate from Prosper. 

And I also make some enhancements by adding chart legend and enabled multiple lines selection, which was suggested from first round feedbacks.

According the second round feedback, I made a few changes ([Updated plot][2]):
  * Adjusted table into one column and moved it to right side of plot.
  * Moved adaptive legend from top right section to left side of plot area with bigger font size and different color.
  * After I had a few friends and family view my plot, they all felt that the highlighted average line did detract from the finding, so I deleted it.
  * It is safe for color-blindness that lines are blue hue, I did confirmed that with a color-blind. 
   [2]: https://bl.ocks.org/purebinary/raw/7a873c9735022ff5707f76e81f465dbe/

After the third round feedback, I make my final visualization ([Final plot][3]):
  * Highlighted the $100,000+ line after animation, and then tender its color legend on the right side. 
  * Changed the tendering orders, now lines tender one by one from the highest rate to the lowest one.
  * Hide the table cells during the animation, so the viewer won't be able to click them during that period.
  * Updated visualization Title. 
  [3]: https://bl.ocks.org/purebinary/raw/bf6363bdc101927258a562ef9614d102/
 
## Feedback   
### First round feedback
  1. Feedback 1:
 > Thanks for sharing this visualization! Here is what I noticed:	
 > * Several of the dependent variables show a dip around the same time frame
 > * Monthly payment and loan amount appear to be correlated, which makes sense.
 > * Monthly income has remained stable after a sharp drop between 2005 and 2006 in sharp contrast to many of the other variables which have oscillated significantly
 > * The buttons work nicely and the plot transitions are smooth. I like how the y-axis range adjusts with the selected data.

 > What I am left wondering is what main finding or findings are intended to be expressed by this visualization. The current visualization seems more exploratory than explanatory. What is your main finding or findings? For P6 it is critical that the visualization be primarily explanatory, though it's great if there is an exploratory element so long as the main focus is explanation. Please let us know what findings are to be conveyed and we can provide guidance on how to adjust the visualization.

  2. Feedback 2:
 > Good job with graph, I have small suggestions from my perspective there are too many lines, so it would be nice if you have a label to see to get a general idea, it would be more convenient than hover on each. 
 
 > Option to select any number of lines to compare with one another would is excellent i guess! Let me know your thoughts!

  3. Feedback 3:
 > Nice chart with author-driven and viewer-driven, I am impressive on all six lines within one graph dynamically demonstrated the changes from 05-14.
 
 > Since all of the lines were set in one graph, the reader can visually see the comparison of the relative trends in different groups, and I noticed:
 > * Interest & Fees and Payments Customer trend is very similar
 > * The trends of Payment Monthly and Amount Loan are also very similar.

### Second round feedback
  1. Feedback 1:    
 > Nice visualization :thumbsup:!
 
 > Here are some things I've notice how you could improve it some more:
 
 > > **attention grabber line-drawing**
 > * I like how the lines run along and the viewer can follow them through time - however it took me really long to realize what the lines actually mean. The section - the adaptive legend in a way - that changes in the top right section is not very obvious and I only saw it while the third or fourth line was drawing itself.
 > * So here I'd suggest to highlight this more in some way. The interesting playful creation of the lines does at the same time draw a lot of attention away from everything else - and in order to understand what's going on it is important that the viewer knows right away what these lines refer to. Then he/she can hop on the :train: right away and enjoy the ride while the line develops :smile:

 > > **line legend**
 > * The second comment is about the clickable legend that explains the different lines on the top left. I find it confusing that it is stacked in pairs of two - I cannot really see the reason why this is the case - especially considering that these are ordinal values - starting small and growing larger in distinct steps.
 > * I think it would fit the data better and avoid confusions, if you'd align it either in one line from left to right (which would fit better into your design, I think) or arrange them in one column.
 > That's it for now!
 
 > You've made a great step into the direction of making the visualization explanatory with the title that you set -it nudges the viewer to think into such an explanatory direction.
 
 > Good job and keep the improvements coming :smile:

  2. Feedback 2:
 > I took a look at the state of your visualization last night and I notice that it has undergone substantial improvement. It's looking really good and I like the smooth animation. Great work!
 
 > It is clear from the visualization that the top income bracket has the consistently lowest borrower rate. It also appears that in general, borrower rate is a function of income. I'm guessing there is more than income here and probably income to debt ratio as well as credit rating, these would all likely be correlated with income.
 
 > I have similar comments as Martin regarding the legend. It might make sense to arrange them in one column and sort them by ascending, they would then generally follow the order of lines in the plot. My guess is that the reason for using the current formatting of the legend table is to save space, one column may make it challenging to see the legend and the plot, all in one window. You may consider playing around with table structure and format, or even position. This could be formatted into a single column and then placed on the right side of the plot. If you do decide to stay with the two column approach I think it would enhance clarity to remove the line separator from the field name (top row, "income range"). With the current separator line it may appear as though the left column is income range and the right column is somehow associated with the left, when in reality these are all income ranges.
 
 > Some things to consider to enhance the explanatory nature of the visualization:
 > * The highlighted grand mean may detract from the finding. My attention is immediately drawn to this and I found myself searching for what income bracket corresponds to the lowest borrower rate. Overall I think it would be best to eliminate the grand mean plot, since it doesn't speak to the finding. and instead highlight the plot with the most consistently low borrower rate (highest income bracket). There may be other approaches, but this is my suggestion. The grand mean would speak more to a finding associated with income brackets consistently falling above or below this mean and may or may not make sense depending on the distribution of the data.
 > * If the visualization is not making use of color blind pallets, please consider this. You would be surprised how often color-blindness can be a barrier to fully understanding a visualization. I always try to include a color-blind feedback provider when making explanatory visualizations, for that very reason.

### Third round feedback
  1. Feedback 1:
 > This is coming together well! It's great that you were able to get feedback from friends and family and thanks for confirming color-blind compatibility. I do have a couple of items to consider:
 > * It's key for this project that a main finding is obvious to the viewer. To that end it may be good to keep the 100,000 + plot highlighted, possibly with a label or that part of the table highlighted. This would direct the audience directly to the finding.
 > * Consider animating per the order of the table, that way we start with the highest rates and descend until we get to the lowest rates. This may help the audience follow the plotting and hone in on the finding.
 > * Consider replacing the word "got", in the title, with "received" or something similar

  2. Feedback from my family:
 > Clicking the table legend could make the lines stop drawing during the animation period.

## Resources

* https://github.com/PMSI-AlignAlytics/dimple/wiki/dimple.chart#constructor
* https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map
* http://bl.ocks.org/duopixel/4063326
* https://gist.github.com/jfreels/6734823
* http://chimera.labs.oreilly.com/books/1230000000345/index.html
* http://www.w3schools.com/


import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    #fig = plt.gcf()
    #fig.set_figheight(4)
    #fig.set_figwidth(4)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1,scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1,mean_scores[-1], str(mean_scores[-1]))
    #plt.show()

#scores = [0,1,0,2,0,3,1,2,3,4,5]
#mean = [0,1,0,1,2,2,2,2,2,3,4]

#plot(scores, mean)
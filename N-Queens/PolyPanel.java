   import javax.swing.*;
   import java.awt.*;
   import java.awt.event.*;
   import java.awt.image.*;
   import java.util.ArrayList;
   import java.util.TreeSet;
    public class PolyPanel extends JPanel
   {
      private static final int FRAME = 400;
      private static final int N = 40;
      private static final int EDGE = 6;
      private static final Color BACKGROUND = new Color(255, 255, 255);
      private BufferedImage myImage;
      private Graphics myBuffer;
      private Timer t;
      public TreeSet<polygon> pop;
       public PolyPanel()
      {
         myImage =  new BufferedImage(FRAME, FRAME, BufferedImage.TYPE_INT_RGB);
         myBuffer = myImage.getGraphics();
         myBuffer.setColor(BACKGROUND);
         myBuffer.fillRect(0, 0, FRAME,FRAME);
	  
	 pop = new TreeSet<polygon>();
	 for(int x = 0; x<N; x++)
		pop.add(create());
         t = new Timer(5, new Listener());
         t.start();
      }
       public void paintComponent(Graphics g)
      {
         g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);
      }
       private class Listener implements ActionListener
      {
          public void actionPerformed(ActionEvent e)
         {
            myBuffer.setColor(BACKGROUND);    //cover the 
            myBuffer.fillRect(0,0,FRAME,FRAME);   //old ball
	    for(polygon poly: pop)
	    {
		   myBuffer.setColor(poly.color); 
		   myBuffer.fillPolygon(poly.vertexx, poly.vertexy, poly.vertexx.length);
	    }
	    
            repaint();
         }
      }
     public polygon create()
    {
	int[] pointsx = new int[EDGE];
	int[] pointsy = new int[EDGE];
	for(int x = 0; x<EDGE; x++)
	{
		pointsx[x] = (int)(Math.random()*FRAME);
		pointsy[x] = (int)(Math.random()*FRAME);
	}
	Color c = new Color((int)(Math.random()*255),(int)(Math.random()*255),(int)(Math.random()*255));
	return new polygon(pointsx,pointsy, c);
    }
   class polygon implements Comparable<polygon>
   {
	int[] vertexx;
	int[] vertexy;
	Color color;
	double rank;
	public polygon(int[] pointsx, int[] pointsy, Color c) 
	{
		vertexx = pointsx;
		vertexy = pointsy;
		color = c;
		rank = 0;
	}
	public int compareTo(polygon two)
	{
		if(rank< two.rank)
			return -1;
		else
			return 1;
	}
   }   
}


/*def h(temp):
	dataset = [[[0,0],[0]],[[1,0],[1]],[[0,1],[1]],[[1,1],[0]]]
	passing = [2]
	temp.append(1)
	passing.extend(temp)
	nn = neuralnet(passing)
	return nn.learnBackUntil(dataset, .001)

def splice(a, b):
	r = randint(1, len(a)-1)
	c = b[:r]+a[r:]
	d = a[:r]+b[r:]
	return c,d

def randomize(a):
			print i
		print len(pop)c = randint(1, 4)
	b = a[:]
	b[randint(0,len(b)-1)] = c
	return b

def genetic(n):
	print 'Start'
	size = n
	die = int(n/4)
	pop = []
	count = 1
	for x in range(0, size):
		temp = create()
		htemp = h(temp)
		pop[len(pop):] = [[htemp, temp]]
	
	pop.sort()
	for i in range(10):
		print i
		pop = pop[:len(pop)-die]
		guess = []                                                                                                  
		for y in range(0, n):
			guess[len(guess):] = range(0, n-y)
		shuffle(guess)
		for x in range(0, int(die/2)):
			temp1,temp2 = splice(pop[guess.pop()][1], pop[guess.pop()][1])
			htemp1, htemp2 = h(temp1),h(temp2)
			for x in range(0, int(die/2)):
				temp1, temp2 = randomize(temp1),randomize(temp2)
				htemp1, htemp2 = h(temp1),h(temp2)
			pop[len(pop):] = [[htemp1, temp1]]
			pop[len(pop):] = [[htemp2, temp2]]
			pop.sort()

	print pop
	print 'End'

genetic(4)*/
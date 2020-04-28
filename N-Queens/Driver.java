   import java.awt.*;
   import javax.swing.*;
   import java.awt.image.*;
    public class Driver
   {
       public static void main(String[] args)
      {
         JFrame frame = new JFrame("Polygon Genetic Algorithm");
         frame.setSize(400, 400);
         frame.setLocation(100, 50);
         frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         frame.setContentPane(new PolyPanel());
         frame.setVisible(true);
      }
   }
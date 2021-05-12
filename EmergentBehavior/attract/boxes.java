import java.util.*;
import java.io.*;
import java.util.*;
import java.lang.*;
import java.awt.Event;
import java.awt.Frame;
import java.awt.Graphics;
import java.awt.Color;

class boxes extends Frame
{
	int xSize;
	int ySize;
    int position = 0;
	Graphics gr;

    public void init()
    {
        xSize = 500;
        ySize = 500;

    	resize(xSize, ySize);
		show();
    }

	public void paint(Graphics g) {
		System.out.print("Handle 'paint' method\n");
		run();
	}

	public void run() {
 	    int x=0;
 	    int y;
	    System.out.print("running\n");
 		gr = getGraphics();

	    try {
	        int blocks_per_row = 5;
	        int num_blocks = 5 * 5;     // 5x5 block grid
	        int block_sz_x = xSize / blocks_per_row;
	        int block_sz_y = ySize / blocks_per_row;

            // Create a grid of blocks
     	    gr.setColor(Color.red);
     	    for (int block = 0; block < num_blocks; block++) {
     	        int xx = block % blocks_per_row;
     	        int yy = (block - xx) / blocks_per_row;
     	        xx = xx * block_sz_x;
     	        yy = yy * block_sz_y;
                if (block % 2 == 0) {
                    gr.fillRect(xx, yy,  block_sz_x, block_sz_y);
                }
                if (block == position) {
             	    gr.setColor(Color.black);
                    gr.fillOval(xx + 10, yy + 10, block_sz_x - 10, block_sz_y - 10);
             	    gr.setColor(Color.red);
                }
     	    }
            position = 7;
            if (position > num_blocks) position = 0;

            // Outline the blocks
     	    gr.setColor(Color.black);
	        for (int row = 0; row < 4; row++)
	        {
                y = (row+1) * ySize / 5;
                x = 0;
                while (x < xSize)
                {
                    gr.drawRect(x, y, 1,1);
                    x++;
                }
	        }
     	    gr.setColor(Color.black);
	        for (int col = 0; col < 4; col++)
	        {
                x = (col+1) * xSize / 5;
                y = 0;
                while (y < ySize)
                {
                    gr.drawRect(x, y, 1,1);
                    y++;
                }
	        }

	    }
	    catch (Exception e) {
    		return;
	    }
	}

	public static void main(String [] args)
	{
		System.out.print("Start boxes\n");
		boxes b = new boxes();
		b.init();
		b.run();
	}
}

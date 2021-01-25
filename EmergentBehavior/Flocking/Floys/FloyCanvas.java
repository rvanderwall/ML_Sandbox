/*
 * FloyCanvas.java
 *
 *  This provides a convas
 *
 * Created on June 15, 2005, 7:44 PM
 */

/**
 *
 * @author  Rob
 */
import java.awt.*;


class FloyCanvas extends Canvas
{
	private boolean reset;
        private FloyField field;

        public FloyCanvas(FloyField theField)
        {
            super();
            field = theField;
            setBackground(Color.black);
            setForeground(Color.white);
            reset = true;
        }        

	public void Clear() {
		reset = true;
		repaint();
	}


	public void paint(Graphics g) {

		int i;
		Floy floy;

		if (reset || !field.ready()) {
			g.setColor(Color.black);
			g.fillRect(0,0,size().width,size().height);
			reset = false;
			return;
		}
                
                Floy[] floys = field.getFloys();
		for (i=0; i<floys.length; i++)
	 	{
			floy = floys[i];
			floy.GetNewNeighbors();
	 		floy.Process();
			floy.Draw(g);
	 	}
	}
}


/*
 * FloyFrame.java
 *
 * Created on June 16, 2005, 7:47 PM
 */

/**
 *
 * @author  Rob
 */
import java.awt.*;

class FloyFrame extends Frame
{
	public FloyFrame(String title) 
	{
		super(title);
                setSize(new Dimension(800,600));
		FloyField f = FloyField.getInstance();
		add(f,BorderLayout.CENTER);
                centerWindow();
		f.start();
	}
        
	public boolean handleEvent(Event e)
	{
		if (e.id == Event.WINDOW_DESTROY)
			System.exit(0);
		return false;
	}

        private void centerWindow()
        {
            //Center the window
            Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
            Dimension frameSize = this.getSize();
            if (frameSize.height > screenSize.height) {
                frameSize.height = screenSize.height;
            }
            if (frameSize.width > screenSize.width) {
                frameSize.width = screenSize.width;
            }
            this.setLocation((screenSize.width - frameSize.width) / 2,
			  (screenSize.height - frameSize.height) / 2);
            this.setVisible(true);
        }

        public static void main(String args[])
	{
		FloyFrame f = new FloyFrame("Floy Flocking");
		f.show();
	}
}
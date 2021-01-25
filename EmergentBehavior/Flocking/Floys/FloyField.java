//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//
//	Modification:	rVanderwall	make it Appl as well as applet
//
//   This holds the behavior for the flock.
//


import java.applet.*;
import java.awt.*;
import java.net.*;


public class FloyField extends Panel implements Runnable {

        public static final int DEFAULT_NUM_FLOYS = 25;
        public static final int DEFAULT_INTERVAL_STEP = 10;

        private Floy[] floys;
        private Object floysLock = new Object();
        
	private Thread runner;
	private FloyCanvas canvas;
	private FloyControl fcontrol;
        
	private Button Start;
	private Button Pause;
	private Button Stop;
	private Button Control;
	private Button Slower;
	private Button Faster;
	private Button Default;
	private Button Invader;
	private Button Quit;
	private Graphics gra;
	private Panel ControlPanel;
	private URL MainPage;
	private Font ButtonFont;

	public int NumFloys;
        public int SleepTime;
        
	private boolean running;
	private boolean dirty;

        private static FloyField theField = null;
        private FloyField(String name)
        {
            super();
            init();
        }
        
        public static FloyField getInstance()
        {
            if (theField == null)
                theField = new FloyField("The Floys");
            return theField;
        }
        
	public void init() {
		ButtonFont = new Font("TimesRoman",Font.PLAIN,12);

		setLayout(new BorderLayout());

		Panel buttonPanel = new Panel();
		Start = new Button(" Start ");
		Pause = new Button(" Pause ");
		Stop = new Button(" Stop ");
		Control = new Button(" Properties ");
		Slower = new Button(" Slower ");
		Faster = new Button(" Faster ");
		Default = new Button(" Default ");
		Invader = new Button(" Invader ");
		Quit = new Button(" Quit ");

		buttonPanel.setFont(ButtonFont);
		buttonPanel.add(Start);
		buttonPanel.add(Pause);
		buttonPanel.add(Stop);
		buttonPanel.add(Control);
		buttonPanel.add(Slower);
		buttonPanel.add(Faster);
		buttonPanel.add(Default);
		buttonPanel.add(Invader);
		buttonPanel.add(Quit);

		add(buttonPanel, BorderLayout.SOUTH);

		canvas = new FloyCanvas(this);
		add(canvas, BorderLayout.CENTER);
		canvas.repaint();
		dirty = true;
                this.useDefaults();
	}

        public boolean ready()
        {
            return !dirty;
        }
        
        public Floy[] getFloys()
        {
            Floy[] clonedFloys;
            synchronized(floysLock)
            {
                clonedFloys = (Floy[])floys.clone();
            }
            return clonedFloys;
        }
        
	public void start()
	{
		if (runner == null)
		{
			runner= new Thread(this);
			runner.start();
			running = true;
		}
	}
	
	public void stop()
	{
		if (runner!=null)
		{
			runner.stop();
			runner=null;
			running = false;
		}
	}

	public void run() {
		int i;
		Floy floy;
		if (dirty) {
                    synchronized(floysLock)
                    {
			floys = new Floy[NumFloys];
			for (i=0; i<NumFloys; i++) {
				floys[i] = new Floy(canvas,Floy.TYPE_FRIEND);
			}
			randomize();
			dirty = false;
                    }
		}
	
		while (true) {
		 	if (Math.random()< (double) Floy.Generic_Free_Will) randomize();
		 	canvas.repaint();
		 	try { Thread.sleep(SleepTime);}
		 	catch (InterruptedException e) {
			}
		}
	}

	public void randomize()
	{
            synchronized (floysLock)
            {
		for (int k=0; k<NumFloys; k++) {
			Floy ng = floys[k];
                        ng.chooseNeighbors(floys);
		}
            }
	}



        
	public boolean action(Event evt, Object o) {

		int i;
		Floy floy;
		boolean rt = false;

		if(evt.target == Quit) {
                    System.exit(0);
		}
		else if (evt.target == Start) {
			start();
			rt = true;
		}

		else if (evt.target == Pause) {
			if (running) {
				stop();
				running = false;
				Pause.setLabel("Continue");
			}
			else {
				start();
				running = true;
				Pause.setLabel("Pause");
			}
			rt = true;
		}

		else if (evt.target == Stop) {
			stop();
			canvas.Clear();
		}

		else if (evt.target == Control) {
			stop();
			canvas.Clear();
			fcontrol = new FloyControl(floys);
		}

		else if (evt.target == Invader) {
                        Floy invader = new Floy(canvas, Floy.TYPE_FOE);
                        synchronized (floysLock) 
                        {
                            dirty=true;
                            floys[0] = invader;
                            invader.chooseNeighbors(floys);
                            dirty=false;
                        }
		}

		else if (evt.target == Default) {
			useDefaults();
			stop();
			dirty = true;
			//showStatus("Default Behavior");
			start();
		}
		else if (evt.target == Slower) {
			if (SleepTime < 10)
				SleepTime++;
			else if (SleepTime < 150)
				SleepTime += 10;
		}
		else if (evt.target == Faster) {
			if (SleepTime > 10)
				SleepTime -= 10;
			else if (SleepTime > 1)
				SleepTime--;
		}
		else {
			rt = true;
		}
		return rt;
	}

        public void useDefaults()
        {
            NumFloys  = DEFAULT_NUM_FLOYS;
            SleepTime = DEFAULT_INTERVAL_STEP;
            dirty = true;
        }

            
	public boolean handleEvent(Event evt) {
		if(evt.id == Event.WINDOW_DESTROY) {
			System.exit(0);
		}
		return super.handleEvent(evt);
	}
}

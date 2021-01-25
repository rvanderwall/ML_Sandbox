//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

import java.applet.*;
import java.awt.*;
import java.net.*;


class GfloyParam {

	float min;
	float max;
	float step;
	float value;
	int nsteps;
	String name;

	public GfloyParam(float mn, float mx, float st, float vl, String nm) {

		min = mn;
		max = mx;
		step = st;
		name = nm;
		value = vl;

		nsteps = (int) ((mx-mn)/step);

	}

	public GfloyParam (float mn, float mx, int ns, float vl, String nm) {

		min = mn;
		max = mx;
		nsteps = ns;
		name = nm;
		value = vl;

		step = (float) ((mx-mn)/nsteps);

	}

	char EncodeValue() {

		int n = (int) ((value - min)/step);
		char k = (char) (64+n);
		return k;

	}

	float DecodeValue(char kar) {

		int n = (int) (kar - 64);
		float k = value + n*step;
		return k;

	}

}


class GfloyCanvas extends Canvas
{
	Image image;
	Color color;
	boolean first;
	boolean reset;

	public GfloyCanvas(Image img)	{

		super();
 		image = img;
		color = Color.white;
		setBackground(Color.black);
		setForeground(Color.white);
		first = true;
		reset = false;

	}

	public GfloyCanvas(Color c)	{

		super();
 		image = null;
		setBackground(Color.black);
		setForeground(Color.white);
		color = c;
		first = true;
		reset = false;

	}

	public void Clear() {

		reset = true;
		repaint();

	}


	public void paint(Graphics g) {

		int i;
		Gfloy Gfloy;

		if (reset) {
			g.setColor(Color.black);
			g.fillRect(0,0,size().width,size().height);
			reset = false;
			return;
		}

		if (image != null)
			g.drawImage(image,0,0,this);
		else {
		}

		for (i=0;i<Gfloys.Gfloys.length;i++)
	 	{
			Gfloy = Gfloys.Gfloys[i];
			Gfloy.GetNeighbors();
	 		Gfloy.Process();
			Gfloy.Draw(g);
	 	}


	}

	Graphics GetGra() {

		return this.getGraphics();
	}
}

public class Gfloys extends Applet implements Runnable {

	Thread runner;
	GfloyCanvas canvas;
	GfloyControl fcontrol;
	static Gfloy[] Gfloys;
	Button Start;
	Button Pause;
	Button Stop;
	Button Control;
	Button Kick;
	Button Slower;
	Button Faster;
	Button Default;
	Button Test;
	Button Quit;
	Graphics gra;
	Panel ControlPanel;
	URL MainPage;
	GfloyParam params[];
	Font ButtonFont;

	int wa,ha,wc,hc;
	int CurrentBehavior;
	boolean running;
	static boolean First;
	static boolean ResetPopulation = true;

	static int NF;
	static int REVDIST;
	static float ACC;
	static float ACCTOMID;	
	static float MAXSPEED;
	static float BOUNCESPEED;
	static float V0;
	static float KICK;
	static int SLEEP;
	static int MARGIN;
	static int NUMNB;
	static int TYPE;
	static String COLOR;


	static AudioClip joy;
	static AudioClip beep;
    static Image picture;
    static AppletContext appcontext;


	public void init() {
		int i;
		Float temp;
		String s;

		ButtonFont = new Font("TimesRoman",Font.PLAIN,12);
		reset();

		s=getParameter("NF");
		if (s==null)
			NF=15;
		else NF = Integer.parseInt(s);
		s=getParameter("REVDIST");
		if (s==null)
			REVDIST=200;
		else REVDIST = Integer.parseInt(s);
		s=getParameter("ACCTOMID");
		if (s==null)
			ACCTOMID=0.1f;
		else {
				temp=new Float(s);
				ACCTOMID = temp.floatValue();
			}
		s=getParameter("ACC");
		if (s==null)
			ACC=0.3f;
		else {
				temp=new Float(s);
				ACC = temp.floatValue();
			}
		s=getParameter("MAXSPEED");
		if (s==null)
			MAXSPEED=5f;
		else {
				temp=new Float(s);
				MAXSPEED = temp.floatValue();
			}
		s=getParameter("BOUNCESPEED");
		if (s==null)
			BOUNCESPEED=.8f;
		else {
				temp=new Float(s);
				BOUNCESPEED = temp.floatValue();
		}

		setLayout(new BorderLayout());

		Panel bot = new Panel();
		Start = new Button(" Start ");
		Pause = new Button(" Pause ");
		Stop = new Button(" Stop ");
		Control = new Button(" Properties ");
		Kick = new Button(" Behavior ");
		Slower = new Button(" Slower ");
		Faster = new Button(" Faster ");
		Default = new Button("Default");
		Test = new Button(" Stranger ");
		Quit = new Button(" Quit ");

		bot.setFont(ButtonFont);

		bot.add(Start);
		bot.add(Pause);
		bot.add(Stop);
		bot.add(Control);
		bot.add(Slower);
		bot.add(Faster);
		bot.add(Default);
		bot.add(Test);
		//bot.add(Quit);
		add("South",bot);

	    appcontext = getAppletContext();
		picture = getImage(getCodeBase(),"Gfloys1.gif");
		joy = getAudioClip(getCodeBase(), "joy.au");
		beep = getAudioClip(getCodeBase(), "Beep.au");

		canvas = new GfloyCanvas(Color.red);
		//canvas = new GfloyCanvas(picture);
		add("Center",canvas);
		canvas.repaint();
		gra = canvas.GetGra();

		CurrentBehavior = 0;
		First = true;

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
		Gfloy Gfloy;

		if (First) {
			hc = canvas.size().height;
			wc = canvas.size().width;
			ha = this.size().height;
			wa = this.size().width;
			String st = EncodeChrom();
			if (ResetPopulation) {
				Gfloys = new Gfloy[NF];
				for (i=0;i<NF;i++) {
						Gfloys[i] = new Gfloy(st,i, wc,hc,0,200,Color.green);
				}
			}
		
			randemize();
			First = false;
		}
	
		gra.setColor(Color.white);
		while (true) {
			/*
			for (i=0;i<NF;i++)
		 	{
				Gfloy = Gfloys[i];
				Gfloy.GetNeighbors();
		 		Gfloy.Process();
				Gfloy.Draw(gra);
				showStatus("x= "+Gfloy.x+" y = "+Gfloy.y+" vx= "+Gfloy.vx+" vy= "+Gfloy.vy);
		 	}
			*/
		 	if (Math.random()< (double) KICK) randemize();
		 	canvas.repaint();
		 	try { Thread.sleep(SLEEP);}
		 	catch (InterruptedException e) {}
		}
		


	}

	public void randemize()
	{
		int i,j,k,n;

		for (k=0;k<NF;k++) {
			Gfloy ng = Gfloys[k];
			for (j=0;j<ng.numnb;j++) {
				n =(int) (Math.random()*NF);
				//if (n == k) {
				//	if (n == 0) n++;
				//	else n--;
				//}
				ng.neighbors[j] = Gfloys[n];
			}
		}
	}


	String EncodeChrom() {

		char kars[];
		String st;

		kars = new char[10];

		kars[0] = (char) ((int) ((int) REVDIST/10) + 64);
		kars[1] = (char) ((int) (64 + ACC*100));
		kars[2] = (char) ((int) (64 + ACCTOMID*100));
		kars[3] = (char) ((int) (64 + MAXSPEED*10));
		kars[4] = (char) ((int) (64 + BOUNCESPEED*100));
		kars[5] = (char) ((int) (64 + V0*10));
		kars[6] = (char) (SLEEP + 64);
		kars[7] = (char) (MARGIN + 64);
		kars[8] = (char) ((int) (64 + NUMNB*10));
		kars[9] = (char) ((int) (64 + TYPE*100));

		st = new String(kars);
		return st;

	}


	void InitParams() {

		params = new GfloyParam[10];

		params[0] = new GfloyParam(0f,500f,50f,200f,"REVDIST");
		params[1] = new GfloyParam(0.1f,1.0f,0.1f,0.3f,"ACC");
		params[2] = new GfloyParam(0.1f,1.0f,0.1f,0.1f,"ACCTOMID");
		params[3] = new GfloyParam(1f,10f,1f,5f,"MAXSPEED");
		params[4] = new GfloyParam(0.2f,2f,0.2f,0.8f,"BOUNCESPEED");
		params[5] = new GfloyParam(1f,10f,1f,4f,"V0");
		params[6] = new GfloyParam(5f,50f,5f,10f,"SLEEP");
		params[7] = new GfloyParam(0f,50f,5f,30f,"MARGIN");
		params[8] = new GfloyParam(0f,10f,1f,2f,"NUMNB");
		params[9] = new GfloyParam(0f,1f,1f,0f,"TYPE");

	}


	String EncodeChrom(GfloyParam params[]) {

		int i;
		char kar;
		String st;
		StringBuffer sb = new StringBuffer(params.length);

		for (i=0;i<params.length;i++) {
			kar = params[i].EncodeValue();
			/*
			int sign =(int) (Math.random()*10);
			int delta =(int) (Math.random()*10);
			if (delta == 1) {
				if (sign > 4) 
					kar = kar++;
				else
					kar = kar--;
			}
			*/
			sb.append(kar);
		}

		st = sb.toString();
		return st;

	}


	static public void reset() {

		NF = 15;
		REVDIST = 200;
		ACC = 0.3f;
		ACCTOMID = 0.1f;	
		MAXSPEED = 5f;
		BOUNCESPEED = 0.8f;
		V0 = 4;
		KICK = (float) 0.05;
		SLEEP = 10;
		MARGIN = 30;
		NUMNB = 2;
		TYPE = 0;

		//showStatus("Default Behavior");

	}


	private void ChangeBehavior(int num) {

		switch (num) {
			case 0:	{
				REVDIST = 200;
				ACC = 0.3f;
				ACCTOMID = 0.1f;	
				MAXSPEED = 5f;
				BOUNCESPEED = 0.8f;
				V0 = 4;
				KICK = (float) 0.05;
				SLEEP = 10;
				MARGIN = 30;
				NUMNB = 2;
				showStatus("Default Behavior");
				break;
			}
			case 1:	{
				REVDIST = 200;
				ACC = 0.05f;
				ACCTOMID = 0.05f;	
				MAXSPEED = 3f;
				BOUNCESPEED = 0.5f;
				V0 = 4;
				KICK = (float) 0.05;
				SLEEP = 10;
				MARGIN = 30;
				NUMNB = 2;
				showStatus("Calm Behavior");
				break;
			}
			case 2:	{
				REVDIST = 200;
				ACC = 0.6f;
				ACCTOMID = 0.2f;	
				MAXSPEED = 5f;
				BOUNCESPEED = 0.8f;
				V0 = 4;
				KICK = (float) 0.05;
				SLEEP = 10;
				MARGIN = 30;
				NUMNB = 2;
				showStatus("Busy Behavior");
				break;
			}
			case 3:	{
				REVDIST = 100;
				ACC = 0.9f;
				ACCTOMID = 0.4f;	
				MAXSPEED = 10f;
				BOUNCESPEED = 2.0f;
				V0 = 4;
				KICK = (float) 0.05;
				SLEEP = 10;
				MARGIN = 30;
				NUMNB = 2;
				showStatus("Frantic Behavior");
				break;
			}

		}

	}

	public boolean action(Event evt, Object o) {

		int i;
		Gfloy Gfloy;
		boolean rt = false;

		if(evt.target == Quit) {
			showStatus("Quit");
			//destroy();
			//System.exit(0);
			try {
				MainPage = new URL("JavaGfloys.html");
				appcontext.showDocument(MainPage);
			}
			catch (MalformedURLException e){
			}
			rt=true;
		}
		else if (evt.target == Start) {
			start();
			//gra.setColor(Color.red);
			//gra.fillRect(10,10,wc-20,hc-20);
			//showStatus("gra color = "+gra.getColor().toString());
			//canvas.repaint();
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
			//First = false;
			fcontrol = new GfloyControl(Gfloys);
			showStatus("Custom Behavior");
			//start();
		}

		else if (evt.target == Test) {
			
			Gfloys[0].type =1;
			Gfloys[0].color = Color.red;
			Gfloys[0].energy = 100;
			Gfloys[0].x = 0;
			Gfloys[0].y = 0;

		}

		else if (evt.target == Default) {
			

			Gfloys[0].type = 0;
			Gfloys[0].color = Color.green;
			Gfloys[0].energy = 100;

			reset();
			stop();
			First = true;
			showStatus("Default Behavior");
			start();

		}

		else if (evt.target == Kick) {
			
			beep.play();
			if (CurrentBehavior == 3)
				CurrentBehavior = 0;
			else
				CurrentBehavior++;
			ChangeBehavior(CurrentBehavior);

			stop();
			First = true;
			start();
		}


		else if (evt.target == Slower) {
			if (SLEEP < 10)
				SLEEP++;
			else if (SLEEP < 150)
				SLEEP += 10;
		}

		else if (evt.target == Faster) {
			if (SLEEP > 10)
				SLEEP -= 10;
			else if (SLEEP > 1)
				SLEEP--;
		}


		else {
			rt = true;
		}

		//showStatus("evt.target= "+evt.target.toString());
		return rt;
	}

	public boolean handleEvent(Event evt) {

		if(evt.id == Event.WINDOW_DESTROY) {
			showStatus("Window Distroy");
			destroy();
			System.exit(0);
		}

		return super.handleEvent(evt);
	}


	private void ScrollbarPanel() {
		ControlPanel = new Panel();
		ControlPanel.setLayout(new GridLayout(2,4));
		Label l1 = new Label("Number of Gfloys");
		Label l2 = new Label("Collision Distance");
		Label l3 = new Label("Acceleration");
		Label l4 = new Label("Adhesion");
		Label l1a = new Label("");
		Label l2a = new Label("");
		Label l3a = new Label("");
		Label l4a = new Label("");
		Scrollbar b1 = new Scrollbar(Scrollbar.HORIZONTAL);
		Scrollbar b2 = new Scrollbar(Scrollbar.HORIZONTAL);
		Scrollbar b3 = new Scrollbar(Scrollbar.HORIZONTAL);
		Scrollbar b4 = new Scrollbar(Scrollbar.HORIZONTAL);
		ControlPanel.add(l1);
		ControlPanel.add(l2);
		ControlPanel.add(l3);
		ControlPanel.add(l4);
		ControlPanel.add(b1);
		ControlPanel.add(b2);
		ControlPanel.add(b3);
		ControlPanel.add(b4);
		add("North",ControlPanel);
	}


}





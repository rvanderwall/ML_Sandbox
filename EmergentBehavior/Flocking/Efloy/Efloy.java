//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

import java.awt.*;

public class Efloy {

	EfloyParam params[];
	EfloyParam fixpars[];
	EfloyParam envpars[];

	String chrom;
	String fixed;
	String environ;

	int	width;
	int	height;
	int	margin;
	int	v0;
	int	sleep;

	int id;
	int	father;
	int	mother;
	int	type;
	Color color;
	int	NumberOfNeighbors;
	float MutationFactor;
	float CrossoverFactor;


	float MaxSpeed;
	float BounceSpeed;
	float ApproachAcceleration;
	float RetreatAcceleration;
	float CenterAcceleration;

	float DistBrotherFactor;
	float DistStrangerFactor;
	float DistLocalFactor;

	int	CollisionDistance;

	float CollisionBrotherFactor;
	float CollisionStrangerFactor;
	float CollisionLocalFactor;

	float MaxEnergyDose;
	float MaxSafetyDose;
	float MaxCooperationDose;

	int	fitness;
	int energy;
	int safety;
	int cooperation;
	float EnergyFactor;
	float SafetyFactor;
	float CooperationFactor;
	float SurviversFactor;

	int PopulationSize;
	float FreeWillFactor;
	int LifeSpan;
	//float SafetyNormalizer;
	Efloy neighbors[];

	float x;
	float y;
	float xtail;
	float ytail;
	float vx;
	float vy;
	float xc;
	float yc;


	public Efloy(EfloyParam pr[], String cr, EfloyParam fp[], String fx,
		EfloyParam ep[], String ev) {

		params = pr;
		fixpars = fp;
		envpars = ep;
		chrom = cr;
		fixed = fx;
		environ = ev;

		DecodeFixed();
		DecodeEnviron();
		//chrom = mutate(false);
		DecodeChrom();
		GetFitness();

		x = (float) Math.random()*(width-margin*2) + margin;
		y = (float) Math.random()*(height-margin*2) + margin;
		xtail = x;
		ytail = y;

		vx = (float) Math.random()*v0-v0/2;
		vy = (float) Math.random()*v0-v0/2;

		neighbors = new Efloy[NumberOfNeighbors];

	}


	private float GetParam(EfloyParam pars[], String st, int pos) {

		float par;
		par = (float) pars[pos].DecodeValue(st.charAt(pos));
		return par;

	}


	private void DecodeChrom() {

	/*
	0. MaxSpeed						5.0		
	1. BounceSpeed					0.8		
	2. ApproachAcceleration			0.3		
	3. RetreatAcceleration			0.3		
	4. CenterAcceleration			0.1		

	5. DistBrotherFactor			1		
	6. DistStrangerFactor			20		
	7. DistLocalFactor				-5		

	8. CollisionDistance			200		

	9. CollisionBrotherFactor		-1		
	10.CollisionStrangerFactor		30		
	11.CollisionLocalFactor			-30		

	*/


		MaxSpeed = GetParam(params,chrom,0);
		BounceSpeed = GetParam(params,chrom,1);
		ApproachAcceleration = GetParam(params,chrom,2);
		RetreatAcceleration = GetParam(params,chrom,3);
		CenterAcceleration = GetParam(params,chrom,4);

		DistBrotherFactor = GetParam(params,chrom,5);
		DistStrangerFactor = GetParam(params,chrom,6);
		DistLocalFactor = GetParam(params,chrom,7);

		CollisionDistance = (int) GetParam(params,chrom,8);

		CollisionBrotherFactor = GetParam(params,chrom,9);
		CollisionStrangerFactor = GetParam(params,chrom,10);
		CollisionLocalFactor = GetParam(params,chrom,11);

	}
	

	private void DecodeFixed() {

	/*
	0. ID							0
	1. Father						0
	2. Mother						0
	3. Type							0 (Local)
	4. Color						5 (Green)
	5. NumberOfNeighbors			2		
	6. MutationFactor				0.01
	7. CrossoverFactor				1.0

    8. energy						100
	9. safety						100
	10.cooperation					100
	11.fitness						200

	*/

		id = (int) GetParam(fixpars,fixed,0);
		father = (int) GetParam(fixpars,fixed,1);
		mother = (int) GetParam(fixpars,fixed,2);
		type = (int) GetParam(fixpars,fixed,3);
		int col = (int) GetParam(fixpars,fixed,4);
		AssignColor(col);
		NumberOfNeighbors = (int) GetParam(fixpars,fixed,5);
		MutationFactor = GetParam(fixpars,fixed,6);
		CrossoverFactor = GetParam(fixpars,fixed,7);

		energy = (int) GetParam(fixpars,fixed,8);
		safety = (int) GetParam(fixpars,fixed,9);
		cooperation = (int) GetParam(fixpars,fixed,10);

		fitness = (int) GetParam(fixpars,fixed,11);
		//GetFitness();

	}


	private void DecodeEnviron() {

	/*
	0. width						0
	1. height						0
	2. margin						0
	3. v0							0
	4. sleep						0

    5. EnergyFactor					100
	6. SafetyFactor					100
	7. CooperationFactor			100
	8. SurviversFactor				10

	9. MaxEnergyDose				10
	10.NaxSafetyDose				10
	11.MaxCooperationDose			10

    12.PopulationSize
	13.FreeWillFactor
	14.LifeSpan


	*/

		width = (int) GetParam(envpars,environ,0);
		height = (int) GetParam(envpars,environ,1);
		margin = (int) GetParam(envpars,environ,2);
		v0 = (int) GetParam(envpars,environ,3);
		sleep = (int) GetParam(envpars,environ,4);

		EnergyFactor = GetParam(envpars,environ,5);
		SafetyFactor = GetParam(envpars,environ,6);
		CooperationFactor = GetParam(envpars,environ,7);
		SurviversFactor = GetParam(envpars,environ,8);


		MaxEnergyDose = GetParam(envpars,environ,9);
		MaxSafetyDose = GetParam(envpars,environ,10);
		MaxCooperationDose = GetParam(envpars,environ,11);

		PopulationSize = (int) GetParam(envpars,environ,12);
		FreeWillFactor = GetParam(envpars,environ,13);
		LifeSpan = (int) GetParam(envpars,environ,14);

	}


	public void GetFitness() {

		fitness = (int) ((energy*EnergyFactor + safety*SafetyFactor + cooperation*CooperationFactor));

	}


	public String mutate() {
 
		int i, sign, delta, flag;
		char kar, old;
		String st=chrom;
		StringBuffer sb = new StringBuffer(chrom.length());

		for (i=0;i<chrom.length();i++) {
			kar = chrom.charAt(i);
			old = kar;

			if (Efloys.Flip(MutationFactor)) {
				kar =(char) (Math.random()*params[i].nsteps+65);
			}
			sb.append(kar);
		}

		st = sb.toString();
		return st;

	}


	private String mutate(boolean GrayCode, float mf) {
 
		int i, sign, delta, flag;
		char kar, old;
		String st=chrom;
		StringBuffer sb = new StringBuffer(chrom.length());

		for (i=0;i<chrom.length();i++) {
			kar = chrom.charAt(i);
			old = kar;

			if (Efloys.Flip(mf)) {
				if (GrayCode) {
					if ((Efloys.Flip((float) 0.5)) && (kar < 250)) 
						kar++;
					else
					if (kar > 65)
						kar--;
				}
				else {
					kar =(char) (Math.random()*params[i].nsteps+65);

				}
			}
			sb.append(kar);

		}

		st = sb.toString();
		return st;

	}

	public void shuffle(boolean Graycode, float mf) {

		chrom = mutate(Graycode,mf);

		DecodeChrom();
		int c = (int) (Math.random()*14+1);
		AssignColor(c);
		if (color == Color.red) 
			type = 1;
		else
			type = 0;

		x = (float) Math.random()*(width-margin*2) + margin;
		y = (float) Math.random()*(height-margin*2) + margin;
		xtail = x;
		ytail = y;

		vx = (float) Math.random()*v0-v0/2;
		vy = (float) Math.random()*v0-v0/2;

	}


	public String CrossOver(String MateChrom) {

		int pos;
		String s1, s2, s;

		pos =(int) (Math.random()*chrom.length());
		s1 = chrom.substring(0,pos);
		s2 = MateChrom.substring(pos);
		s = s1.concat(s2);

		/*
		Efloys.deb.showMsg("   ");
		Efloys.deb.showMsg("======= New =======");
		Efloys.deb.showMsg("s1 = "+s1+" s2= "+s2+" pos= "+pos+" s= "+s);
		*/
		return s;

	}


	public int dist(Efloy ng)
	{
		int d,d1,d2;
		d1=(int)(x-ng.x);
		d2=(int)(y-ng.y);
		d=d1*d1+d2*d2;
		return(d);
	}
	

	public String GetColorName() {

		String s;

		if (color == Color.black) s = "BLACK";
		else if (color == Color.blue) s = "BLUE";
		else if (color == Color.cyan) s = "CYAN";
		else if (color == Color.darkGray) s = "DARKGRAY";
		else if (color == Color.gray) s = "GRAY";
		else if (color == Color.green) s = "GREEN";
		else if (color == Color.lightGray) s = "LIGHTGRAY";
		else if (color == Color.magenta) s = "MAGENTA";
		else if (color == Color.orange) s = "ORANGE";
		else if (color == Color.pink) s = "PINK";
		else if (color == Color.red) s = "RED";
		else if (color == Color.white) s = "WHITE";
		else if (color == Color.yellow) s = "YELLOW";
		else s = "GREEN";

		return s;

	}


	public int GetColorNumber() {

		int s;

		if (color == Color.black) s = 0;
		else if (color == Color.blue) s = 1;
		else if (color == Color.cyan) s = 2;
		else if (color == Color.darkGray) s = 3;
		else if (color == Color.gray) s = 4;
		else if (color == Color.green) s = 5;
		else if (color == Color.lightGray) s = 6;
		else if (color == Color.magenta) s = 7;
		else if (color == Color.orange) s = 8;
		else if (color == Color.pink) s = 9;
		else if (color == Color.red) s = 10;
		else if (color == Color.white) s = 11;
		else if (color == Color.yellow) s = 12;
		else s = 5;

		return s;

	}

	public String GetTypeName() {

		String s;

		if (type == 0) s = "Local";
		else if (type == 1) s = "Stranger";

		else s = "Local";

		return s;

	}


	public void AssignColor(String c) {

		if (c.equals("BLACK")) color = Color.black;
		else if (c.equals("BLUE")) color = Color.blue;
		else if (c.equals("CYAN")) color = Color.cyan;
		//else if (c.equals("DARKGRAY")) color = Color.darkGray;
		else if (c.equals("GRAY")) color = Color.gray;
		else if (c.equals("GREEN")) color = Color.green;
		else if (c.equals("LIGHTGRAY")) color = Color.lightGray;
		else if (c.equals("MAGENTA")) color = Color.magenta;
		else if (c.equals("ORANGE")) color = Color.orange;
		else if (c.equals("PINK")) color = Color.pink;
		else if (c.equals("RED")) color = Color.red;
		else if (c.equals("WHITE")) color = Color.white;
		else if (c.equals("YELLOW")) color = Color.yellow;
		else color = Color.green;

	}


	public void AssignColor(int n) {

		if (n == 0) color = Color.black;
		else if (n == 1) color = Color.blue;
		else if (n == 2) color = Color.cyan;
		//else if (n == 3) color = Color.darkGray;
		else if (n == 4) color = Color.gray;
		else if (n == 5) color = Color.green;
		else if (n == 6) color = Color.lightGray;
		else if (n == 7) color = Color.magenta;
		else if (n == 8) color = Color.orange;
		else if (n == 9) color = Color.pink;
		else if (n == 10) color = Color.red;
		else if (n == 11) color = Color.white;
		else if (n == 12) color = Color.yellow;
		else color = Color.green;

	}


	public void GetNeighbors()
	{
		int i,j,k;
		Efloy ng;

		for (i=0;i<NumberOfNeighbors;i++) {
			ng=neighbors[i];
			for (j=0;j<NumberOfNeighbors;j++) {
				if (dist(ng.neighbors[j]) < dist(ng))
					neighbors[i]=ng.neighbors[j];
				if (ng.neighbors[j].type == 1)
					neighbors[i]=ng.neighbors[j];
			}
		}

		xc = 0;
		yc = 0;
		for (k=0;k<NumberOfNeighbors;k++) {
			if (neighbors[k] == this) neighbors[k]=neighbors[k].neighbors[0];
			xc += neighbors[k].x;
			yc += neighbors[k].y;
		}
		xc = xc/NumberOfNeighbors;
		yc = yc/NumberOfNeighbors;
	}


	public void Process() {
	
		int rev;
		int i;
		int d;
		int SafetyAddition;

		xtail = x;
		ytail = y;
		rev = -1;
		
		for (i=0;i<NumberOfNeighbors;i++) {
			
			d = dist(neighbors[i]);

			if (d == 0)
				rev = 0;
			else if (d < CollisionDistance) {
				if (neighbors[i].type != type) {
					if (type == 1) {
						energy--;
						rev = (int) CollisionLocalFactor;
						if (energy < 0) energy = 0;
						if (Efloys.CurrentGeneration > 0) 
							Efloys.appcontext.showStatus("Generation #" + Efloys.CurrentGeneration+"  Stranger's remainig energy: "+energy);
						else
							Efloys.appcontext.showStatus("Stranger's remainig energy: "+energy);
					}
					else  {
						energy += (int) MaxEnergyDose;
						rev = (int) CollisionStrangerFactor;
					}
				}
				else { 
					safety += (int) MaxSafetyDose;
				    rev = (int) CollisionBrotherFactor;
				}
			}
			else  {
				if (type == 1)
					rev = (int) DistLocalFactor;
				else if (neighbors[i].type == 1) 
					rev = (int) DistStrangerFactor;
				else {
					SafetyAddition = (int) ((MaxSafetyDose*CollisionDistance)/(d+CollisionDistance));
				    safety += SafetyAddition;
					rev = (int) DistBrotherFactor;
				}
			}

			if (x < neighbors[i].x)
				vx += ApproachAcceleration*rev;
			else
				vx -= ApproachAcceleration*rev;

			if (y < neighbors[i].y)
				vy += ApproachAcceleration*rev;
			else
				vy -= ApproachAcceleration*rev;
		}
	

		if (vx > MaxSpeed) vx = MaxSpeed;
		if (vx < -MaxSpeed) vx = -MaxSpeed;
		if (vy > MaxSpeed) vy = MaxSpeed;
		if (vy < -MaxSpeed) vy = -MaxSpeed;

		if (x < 1) vx = BounceSpeed;
		if (x > (width-3)) vx = -BounceSpeed;
		//if (xtail > (width-3)) vx = -BounceSpeed;
		if (y < 1) vy = BounceSpeed;
		if (y > (height-1)) vy = -BounceSpeed;
		
		if (type == 0) {
			float v = (float) (Math.sqrt(vx*vx + vy*vy));
			energy += (int) (v/MaxSpeed*MaxEnergyDose);
			if (x < width/2) vx += CenterAcceleration;
			if (x > width/2) vx -= CenterAcceleration;
			if (y < height/2) vy += CenterAcceleration;
			if (y > height/2) vy -= CenterAcceleration;
		}

		x += vx;
		y += vy;
		if (energy < 1)	{
			if (Efloys.WithSound)
				Efloys.joy.play();
			color = Color.green;
			type = 0;
			energy = 10;
			safety = 10;
			cooperation = 10;
			Efloys.NewGeneration = true;
		}

		GetFitness();

	}


	public void Draw(Graphics g) {

		g.setColor(color);

		if (Efloys.DrawNumbers)
			g.drawString(""+id,(int) x, (int) y);
		else {
			g.drawLine((int) xtail, (int) ytail,(int) x,(int) y);
			g.fillOval((int) x, (int) y, 3, 3);
		}


	}

}

/*

1. ID							0
2. Father						0
3. Mother						0

4. Type							0 (Local)
5. Color						5 (Green)
6. NumberOfNeighbors			2		
7. MutationFactor				0.01
8. CrossoverFactor				1.0

9. MaxSpeed						5.0		
10.BounceSpeed					0.8		
11.ApproachAcceleration			0.3		
12.RetreatAcceleration			0.3		
13.CenterAcceleration			0.1		

14.DistBrotherFactor			1		
15.DistStrangerFactor			20		
16.DistLocalFactor				-5		

17.CollisionDistance			200		

18.CollisionBrotherFactor		-1		
19.CollisionStrangerFactor		30		
20.CollisionLocalFactor			-30		

21.MaxEnergyDose				10
22.MaxSafetyDose				10
23.MaxCooperationDose			10

24.Sleep						10
25.Margin						0
26.V0							4

*/


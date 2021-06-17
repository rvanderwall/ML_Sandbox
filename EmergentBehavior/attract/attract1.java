import java.util.*;



class attract1 
{

	public static void main(String [] args)
	{
		System.out.print("Start\n");
		double start=Double.valueOf(args[0]).doubleValue();
		//double c = 2.0;
		double c = 3.2;
		double x = start;

		for (int iter=0; iter < 10; iter++)
		{
			x = c * x * (1-x);
			System.out.print("iteration " + iter + " x=" + x + "\n");
		}
	}
}

public class App {
    public static int max(int n, int m) {
        if (n>m)
            return n;
        else
            return m;
    }

    public static void main(String[] args) {
        System.out.println("The maximum of 2 and 1 is " + max(2,1));
    }
}

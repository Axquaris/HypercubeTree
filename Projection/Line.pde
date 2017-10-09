
class Line {
  Point p1;
  Point p2;
  
  Line(float[] v1, float[] v2) {
    p1 = new Point(v1);
    p2 = new Point(v2);
  }
  
  Line(Point ip1, Point ip2) {
     p1 = ip1;
     p2 = ip2;
  }
  
  void rotate(int a1, int a2, float angleD) {
    p1.rotate(a1, a2, angleD);
    p2.rotate(a1, a2, angleD);
  }
  
  void draw() {
    line(p1.v2[0], p1.v2[1], p2.v2[0], p2.v2[1]);
  }
  
  boolean equals(Line o) {
    return p1.equals(o.p1) && p2.equals(o.p2);
  }
}
class Point {
  int n;
  float[] vN;
  float[] v2;
  
  public Point(float[] inD) {
    vN = inD;
    n = vN.length;
    
    updateV2();
  }
  
  void updateV2() {
    if (vN.length == 2) {
      v2 = vN;
      return;
    }
    
    float[] vX = new float[n];
    float[] vY = new float[n];
    
    vX[0] = 1;
    vX[1] = 0;
    vY[0] = 0;
    vY[1] = 1;
    
    float cX = dot(vN, vX) / dot(vX, vX);
    float cY = dot(vN, vY) / dot(vY, vY);
    
    v2 = new float[2];
    v2[0] = cX;
    v2[1] = cY;
  }
  
  // ROTATES ABOUT THE ORIGIN a1 => X, a2 => Y
  void rotate(int a1, int a2, float angleD) {
    float angle = atan2(vN[a2], vN[a1]);
    float magnitude = sqrt(vN[a1]*vN[a1] + vN[a2]*vN[a2]);
    
    vN[a1] = magnitude*cos(angle+angleD);
    vN[a2] = magnitude*sin(angle+angleD);
    
    updateV2();
  }
  
  float dot(float[] a, float[] b) {
    float sum = 0;
    
    for (int i = 0; i < a.length; i++) {
      sum += a[i] * b[i];
    }
    
    return sum;
  }
  boolean equals(Point o) {
    for (int i = 0; i < vN.length; i++) {
      if (vN[i] != o.vN[i])
        return false;
    }
    return true;
  }
}
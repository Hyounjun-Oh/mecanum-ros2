function q = rotation2quaternion(rotation_mat)
    
    mat = rotation_mat;
    w = sqrt(1 + mat(1,1) + mat(2,2) + mat(3,3))/2;
    x = (mat(3,2) - mat(2,3))/4*w;
    y = (mat(1,3) - mat(3,1))/4*w;
    z = (mat(2,1) - mat(1,2))/4*w;

    q = [w,x,y,z];

end
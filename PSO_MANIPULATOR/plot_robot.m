% Plot Manipulator from Homogeneous Matrix
% Hyounjun Oh

function plot_robot(T)
    
    for iter = 1:length(T)+1
        if iter == 1
            plot_x(iter) = 0;
            plot_y(iter) = 0;
            plot_z(iter) = 0;
        else
            plot_x(iter) = T(iter-1).multiple_transform(1,4);
            plot_y(iter) = T(iter-1).multiple_transform(2,4);
            plot_z(iter) = T(iter-1).multiple_transform(3,4);
        end
    end
    plot3(plot_x, plot_y, plot_z, '-or',"LineWidth",3);
    axis([-1000,1000,-1000,1000,-500,2000]);
    hold on
    grid on
    pause(2)
end
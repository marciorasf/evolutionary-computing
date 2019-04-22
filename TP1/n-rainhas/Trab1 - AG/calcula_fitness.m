function [fitness] = calcula_fitness(individuo)
% retorna o numero de colisoes
% o maximo de colisoes e n*(n-1)/2 para um tabuleiro nxn
    fitness = 0;
    n = length(individuo);
    for i = 1:n
        for j = 1:n
            if ((abs(i-j)== abs(individuo(i)-individuo(j))) && (i ~= j))
                fitness = fitness+1;               
            end
        end
    end
    fitness = fitness/2;  
endfunction

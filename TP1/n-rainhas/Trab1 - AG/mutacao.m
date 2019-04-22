function [filhosMutados] = mutacao(filhos)
    dimFilhos = size(filhos);
    for i = 1:dimFilhos(1)
        posPermut = randperm(dimFilhos(2),2);
        aux = filhos(i,posPermut(1));
        filhos(i,posPermut(1)) = filhos(i,posPermut(2));
        filhos(i,posPermut(2)) = aux;
    end
    
    filhosMutados = filhos;
end
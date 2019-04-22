clear
% Numero de rainhas, ou dimensao do tabuleiro
n_tabuleiro = 20;

% Tamanho da populacao
tam_pop = 100;

% Numero de Geracoes
n_ger = 100;

gen = 1;

% Gerar populacao inicial
for i = 1:tam_pop
    pop(i,:) = randperm(n_tabuleiro,n_tabuleiro);
end

% coloca o fitness de cada individuo em sua coluna n+1
for i = 1:tam_pop
    pop(i,n_tabuleiro+1) = calcula_fitness(pop(i,1:n_tabuleiro));
end

melhorFitness(1) = pop(1,n_tabuleiro+1);
mediaFitness(1) = sum(pop(:,n_tabuleiro+1))/tam_pop;

% Inicializa os pais que cruzarao
paisACruzar = zeros(5,n_tabuleiro+1);

% processo de evolução da espécie
% É finalizado caso seja alcançado o número máximo de gerações ou a média
% do fitness dos indivíduos seja nula
if melhorFitness(gen) ~= 0
    for gen = 2:n_ger+1
        % Selecao dos pais
        posFitPais = randperm(tam_pop,5);
        for i = 1:5
            paisACruzar(i,:) = pop(posFitPais(i),:);
        end

        % Ordenacao dos pais por fitness
        paisACruzar = sortrows(paisACruzar,n_tabuleiro+1);

        % Matriz com os pais selecionados
        melhoresPais = [paisACruzar(1,:); paisACruzar(2,:)];

        % Geracao dos descendentes
        proximaGeracao = CutAndCrossfill_Crossover(melhoresPais(:,1:n_tabuleiro));
        pMut = rand;
        if pMut < 0.8
            proximaGeracao = mutacao(proximaGeracao);
        end
        proximaGeracao(:,n_tabuleiro+1) = [calcula_fitness(proximaGeracao(1,:)) calcula_fitness(proximaGeracao(2,:))];

        % Adicao dos filhos na populacao
        pop(tam_pop+1,:) = proximaGeracao(1,:);
        pop(tam_pop+2,:) = proximaGeracao(2,:);

        % Ordena a populacao pelo fitness e retira os dois piores
        pop = sortrows(pop,n_tabuleiro+1);
        pop(tam_pop+2,:) = [];
        pop(tam_pop+1,:) = [];

        % Incrementa os parametros para avaliacao da evolucao da populacao
        melhorFitness(gen) = pop(1,n_tabuleiro+1);
        mediaFitness(gen) = sum(pop(:,n_tabuleiro+1))/tam_pop;
        if melhorFitness(gen) == 0
            break
        end
    end
end
figure(1)
plot(1:gen,melhorFitness)
title('Melhor Fitness por Geração')
xlabel('Geração')
ylabel('Melhor Fitness')

figure(2)
plot(1:gen,mediaFitness)
title('Media dos Fitness por Geração')
xlabel('Geração')
ylabel('Media Fitness')
melhorFitness(gen)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% programme qui calcule le niveau sonore par bande n-i�me d'octave � partir 
% d'un spectre en bandes fines. Trace le spectre en bandes fines et n-i�me d'octave
% NB : filtres non noramlis�s. Coupure brute.
%
% Auteur :  C. Ayrault, mars 2012
% Mise � jour : f�vrier 2018
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear   
close all


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Donn�es 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


load('BLANC_1.lvm') % A REMPLACER PAR LE LOAD DU SPECTRE
t=BLANC_1(:,1);     % ....

fe=1/(t(2)-t(1));   % A SUPPRIMER
N=length(t);        % A SUPPRIMER
f=[0:N-1]/N*fe;     % A REMPLACER PAR LE LOAD DU VECTEUR F
x=BLANC_1(:,2);     % A SUPPRIMER
x=x-mean(x);        % A SUPPRIMER


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Analyse frequentielle par Bandes 
%
%           on ne normalise pas le spectre
%           on calcule un niveau par bande c
%           pour le calcul du niveau global, on divise la valeur efficace par N 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% fr�quences centrales des bandes
N_oct=input('entrer le nombre N-i�me d''octave souhait� (1 pour octave, 3 pour tiers d''octave ...) : ')
fc=[31.25*2.^([1:10*N_oct]/N_oct)];         
fcmin=fc/2^(1/(2*N_oct));
fcmax=fc*2^(1/(2*N_oct));

% calcul de l'energie pour chaque frequence, puis dans chaque bande (somme) puis globale (somme)
y=abs(fft(x)); % A SUPPRIMER SI LOAD DU SPECTRE 

figure(3)
semilogx(f(1:N/2),20*log10(y(1:N/2)/20e-6*sqrt(2)/N)) 
grid on
xlabel('Fr�quence (Hz)')
ylabel('Niveau (dB)')
title('Spectre calcul� � partir de l''�nergie dans chaque bande')

Et=0;   % �nergie totale initiale 
for i=1:length(fc)
    deb(i)=max(find(f<=fcmin(i)));
    fin(i)=max(find(f<=fcmax(i)));
    yi=y(deb(i):fin(i));
    Ni=length(yi);
    Ei=sum(yi.^2);              % energie non normalisee
    Ayi=sqrt(Ei);               % amplitude non normalisee
    vectAyi=Ayi*ones(1,Ni);
    vectBO(i)=Ayi;
    fi=f(deb(i):fin(i));
    
    figure(3)
    % si on veut le niveau en dB SPL dans chaque bande
    hold on
    semilogx(fi,20*log10(vectAyi/20e-6*sqrt(2)/N),'r')
    legend('niveau bande fine (dB SPL)','niveau en bande d''octave (dB SPL)')
    
    Et=Ayi^2+Et;                % somme des energies
end

% valeur efficace du signal caclcul�e dans le domaine fr�quentiel
sig5=sqrt(Et*2/N^2);            % normalisation des energies avant calcul de l'et
                                % energie*2 pour la partie repliee 
L25=20*log10(sig5/20e-6);
fprintf('Niveau sonore global : %3.4f dB \n',L25)

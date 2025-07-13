import CoolProp.CoolProp as CP
import os
import numpy as np
import matplotlib.pyplot as plt

def diagram_z(substance, P_crit, T_crit, Pr, Tr, P, T):
    Tr_list = [0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.2, 1.3, 1.5, 2, 5]

    plt.figure(figsize=(10, 6))
    plt.title('Fator de compressibilidade para o fluido de Lee-Kesler simples', fontsize=12)
    plt.suptitle(f'{substance}')
    plt.xlabel(f'Pressão reduzida, $P_r$')
    plt.ylabel(f'Fator de compressibilidade, $Z$')
    plt.grid(True, linestyle='--', alpha=0.7)

    for Tr_itens in Tr_list:
        Pr_array = np.linspace(0.01, 10, 1000)
        Z_array = []

        for Pr_itens in Pr_array:
            P_list = Pr_itens*P_crit
            T_list = Tr_itens*T_crit
            try:
                Z = CP.PropsSI('Z', 'P', P_list, 'T', T_list, substance)
                Z_array.append(Z)
            except:
                Z_array.append(np.nan)

        plt.plot(Pr_array, Z_array, label=f'$T_r$ = {Tr_itens}')

    Z_coordinate = CP.PropsSI('Z', 'P', P, 'T', T, substance)
    print(f'\nPressão reduzida [-] = {Pr}\nTemperatura reduzida [-] = {Tr}\nFator de compressibilidade [-] = {Z_coordinate:.5f}')
    plt.scatter(Pr, Z_coordinate, color='black', s=10, zorder=3)
    plt.annotate(f'$Z$={Z_coordinate:.2f}, $T_r$={Tr:.2f}, $P_r$={Pr:.2f}', 
                (Pr, Z_coordinate),
                textcoords="offset points",
                xytext=(5,5),
                ha='left',
                bbox=dict(
                    boxstyle='square',
                    facecolor='white',
                    edgecolor='black'
                )
    )
    plt.legend()
    plt.xscale('log')
    plt.xlim(0.01, 10)
    plt.ylim(0, 1.3)
    plt.show()

def ThermalProperties():
    print('-----Propriedades Termodinâmicas-----\n')
    
    substance = input('Substância: ').upper()
    P = float(input('\nPressão [Pa]: '))
    T = float(input('Temperatura [K]: '))

    rho = CP.PropsSI('D', 'P', P, 'T', T, substance)
    h = CP.PropsSI('H', 'P', P, 'T', T, substance)
    s = CP.PropsSI('S', 'P', P, 'T', T, substance)
    Z = CP.PropsSI('Z', 'P', P, 'T', T, substance)
    U = CP.PropsSI('U', 'P', P, 'T', T, substance)

    print(f'\nMassa específica [kg/m^3] = {rho}\nVolume específico [m^3/kg] = {1/rho}\nEntalpia [kJ/kg] = {h}\nEnergia interna [kJ/kg] = {U}\nEntropia [kJ/K] = {s}\nFator de compressibilidade = {Z}')

def factor_z():
    print('-----Fator de Compressibilidade-----\n')

    option_z = input('1 - Pressão [Pa] e temperatura [K]\n2 - Temperatura [K] e volume específico [m^3/kg]\n\nIndique quais variáveis tem disponível: ')
    substance = input('\nSubstância: ').upper()
    P_crit = CP.PropsSI(substance, 'Pcrit')
    T_crit = CP.PropsSI(substance, 'Tcrit')

    R = CP.PropsSI('GAS_CONSTANT', substance) / CP.PropsSI('MOLAR_MASS', substance)

    if option_z == '1':
        P = float(input('Pressão [Pa]: '))
        T = float(input('Temperatura [K]: '))
        rho = CP.PropsSI('D', 'P', P, 'T', T, substance)
        v = 1 / rho

    elif option_z == '2':
        v = float(input('Volume específico [m^3/kg]: '))
        T = float(input('Temperatura [K]: '))
        rho = 1/v
        P = CP.PropsSI('P', 'D', rho, 'T', T, substance)

    Pr = P/P_crit
    Tr = T/T_crit
    diagram_z(substance, P_crit, T_crit, Pr, Tr, P, T)

while True:
    try:
        print('\n-----Ferramenta Termodinâmica-----\n')
        option = input('1 - Fator de Compressibilidade \n2 - Propriedades de uma substância pura\n\nIndique o que deseja obter: ')

        if option == '1':
            os.system('clear')
            factor_z()
        if option == '2':
            os.system('clear')
            ThermalProperties()

    except (ValueError, KeyboardInterrupt, TypeError) as exception:
        print(f'\n\nErro inesperado: {exception}')

    continuar = input('\nCalcular novamente (S/N): ').lower().strip()
    if continuar != 's':
        os.system('clear')
        print('-----Programa encerrado-----\n')
        break
    else:
        os.system('clear')
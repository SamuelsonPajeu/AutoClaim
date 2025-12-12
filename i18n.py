translations = {
    'pt_BR': {
        # checkUserStatus patterns
        'check_can_marry': 'você __pode__ se casar agora mesmo',
        'check_marry_cooldown': r'antes que você possa se casar novamente \*\*((?:\d+h )?\d+)\*\* min',
        'check_next_reset': r'reinicialização é em \*\*((?:\d+h )?\d+)\*\* min',
        'check_rolls_remaining': r'Você tem \*\*(\d+)\*\* rolls restantes',
        'check_dk_ready': '$dk está pronto!',
        'check_dk_cooldown': 'O próximo $dk em',
        
        # Logs - checkUserStatus
        'log_checking_status': 'Verificando status do usuário...',
        'log_can_marry_now': 'Pode se casar agora',
        'log_time_until_marry': 'Tempo até casar',
        'log_rolls_remaining': 'Rolls restantes',
        'log_dk_available': '$dk disponível',
        
        # Logs - processCard
        'log_trying_claim': 'Trying to Claim',
        'log_anti_steal': 'Zé povinho aqui não ✋🚫, anti roubo ativado',
        'log_waiting_single': 'Esposa(o) de alguém detectada(o). Esperando ficar solteira 😋...',
        'log_has_kakera': 'Has kakera',
        'log_trying_react_kakera': 'Trying to react to',
        'log_kakera_of': 'of',
        
        # Logs - simpleRoll
        'log_rolling_at': 'Rolling at',
        'log_snooze_active': 'Snooze ativo: {hour:02d}h está entre {begin:02d}h e {end:02d}h. Ignorando execução.',
        'log_no_rolls': 'Nenhum roll disponível. Pulando execução.',
        'log_dk_available_exec': '$dk disponível! Executando claim...',
        'log_dk_daily_done': '$dk e $daily executados.',
        'log_marry_active': 'marryLastRoll: ATIVO - Casará no último roll se nenhum for claimado',
        'log_divorce_active': 'divorceLastRoll: ATIVO - Divorciará após casar',
        'log_marry_inactive': 'marryLastRoll: INATIVO - Tempo até casar deve ser menor que 1h (atual: {time})',
        'log_invalid_message': 'Mensagem inválida detectada (erro {count}/{max}), verificando status...',
        'log_error_limit': 'Limite de erros atingido.',
        'log_no_rolls_after_check': 'Nenhum roll disponível após verificação.',
        'log_applying_marry': 'Aplicando marryLastRoll: {name} (Power: {power})',
        'log_divorcing': 'Divorciando {name}...',
        'log_divorce_complete': 'Divorce completo.',
        'log_rolling_ended': 'Rolling ended',
        'log_trying_pokeslot': 'Trying to roll Pokeslot',
        
        # Logs - Bot.py
        'log_bot_started': 'Bot iniciado',
        'log_random_execution': 'Execução aleatória: entre XX:{min} e XX:{max}',
        'log_fixed_execution': 'Execução fixa: a cada hora no minuto {min}',
        'log_next_execution': 'Próxima execução agendada para: XX:{minute:02d}',
        'log_next_execution_full': 'Próxima execução agendada para: {hour:02d}:{minute:02d}',
    },
    
    'en': {
        # checkUserStatus patterns
        'check_can_marry': 'you __can__ claim right now',
        'check_marry_cooldown': r"you can't claim for another \*\*((?:\d+h )?\d+)\*\* min",
        'check_next_reset': r'next claim reset is in \*\*((?:\d+h )?\d+)\*\* min',
        'check_rolls_remaining': r'You have \*\*(\d+)\*\* rolls left',
        'check_dk_ready': '$dk is ready!',
        'check_dk_cooldown': 'The next $dk in',
        
        # Logs - checkUserStatus
        'log_checking_status': 'Checking user status...',
        'log_can_marry_now': 'Can marry now',
        'log_time_until_marry': 'Time until marry',
        'log_rolls_remaining': 'Rolls remaining',
        'log_dk_available': '$dk available',
        
        # Logs - processCard
        'log_trying_claim': 'Trying to Claim',
        'log_anti_steal': 'Not your roll ✋🚫, anti-steal activated',
        'log_waiting_single': 'Someone\'s waifu/husbando detected. Waiting to become single 😋...',
        'log_has_kakera': 'Has kakera',
        'log_trying_react_kakera': 'Trying to react to',
        'log_kakera_of': 'of',
        
        # Logs - simpleRoll
        'log_rolling_at': 'Rolling at',
        'log_snooze_active': 'Snooze active: {hour:02d}h is between {begin:02d}h and {end:02d}h. Skipping execution.',
        'log_no_rolls': 'No rolls available. Skipping execution.',
        'log_dk_available_exec': '$dk available! Executing claim...',
        'log_dk_daily_done': '$dk and $daily executed.',
        'log_marry_active': 'marryLastRoll: ACTIVE - Will marry on last roll if none claimed',
        'log_divorce_active': 'divorceLastRoll: ACTIVE - Will divorce after marry',
        'log_marry_inactive': 'marryLastRoll: INACTIVE - Time until marry must be less than 1h (current: {time})',
        'log_invalid_message': 'Invalid message detected (error {count}/{max}), checking status...',
        'log_error_limit': 'Error limit reached.',
        'log_no_rolls_after_check': 'No rolls available after check.',
        'log_applying_marry': 'Applying marryLastRoll: {name} (Power: {power})',
        'log_divorcing': 'Divorcing {name}...',
        'log_divorce_complete': 'Divorce complete.',
        'log_rolling_ended': 'Rolling ended',
        'log_trying_pokeslot': 'Trying to roll Pokeslot',
        
        # Logs - Bot.py
        'log_bot_started': 'Bot started',
        'log_random_execution': 'Random execution: between XX:{min} and XX:{max}',
        'log_fixed_execution': 'Fixed execution: every hour at minute {min}',
        'log_next_execution': 'Next execution scheduled for: XX:{minute:02d}',
        'log_next_execution_full': 'Next execution scheduled for: {hour:02d}:{minute:02d}',
    },
}

def get_text(key, lang='pt_BR', **kwargs):
    """
    Obtém o texto traduzido para a chave especificada
    
    Args:
        key: Chave da tradução
        lang: Código do idioma (pt_BR, en)
        **kwargs: Parâmetros para formatação de string
    
    Returns:
        String traduzida e formatada
    """
    if lang not in translations:
        lang = 'pt_BR'
    
    text = translations[lang].get(key, translations['pt_BR'].get(key, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text

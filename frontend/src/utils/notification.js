// Função para tocar som de notificação
export const playNotificationSound = () => {
  try {
    // Criar um contexto de áudio
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    // Criar oscilador para gerar o som
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Configurar o som (frequência e tipo)
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime); // Frequência alta
    
    // Configurar volume com fade
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    // Tocar o som
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
    
    // Segunda nota (tom mais alto)
    setTimeout(() => {
      const oscillator2 = audioContext.createOscillator();
      const gainNode2 = audioContext.createGain();
      
      oscillator2.connect(gainNode2);
      gainNode2.connect(audioContext.destination);
      
      oscillator2.type = 'sine';
      oscillator2.frequency.setValueAtTime(1000, audioContext.currentTime);
      
      gainNode2.gain.setValueAtTime(0.3, audioContext.currentTime);
      gainNode2.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
      
      oscillator2.start(audioContext.currentTime);
      oscillator2.stop(audioContext.currentTime + 0.2);
    }, 100);
    
  } catch (error) {
    console.error('Erro ao tocar som de notificação:', error);
  }
};

// Solicitar permissão para notificações do navegador
export const requestNotificationPermission = async () => {
  if ('Notification' in window && Notification.permission === 'default') {
    await Notification.requestPermission();
  }
};

// Mostrar notificação do navegador
export const showBrowserNotification = (title, options = {}) => {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, {
      icon: '/logo192.png',
      badge: '/logo192.png',
      ...options
    });
  }
};

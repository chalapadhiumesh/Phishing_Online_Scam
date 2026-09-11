export const getRiskColor = (riskLevel) => {
  switch (riskLevel?.toUpperCase()) {
    case 'LOW':
      return 'var(--success)';
    case 'MEDIUM':
      return 'var(--warning)';
    case 'HIGH':
      return 'var(--danger)';
    case 'CRITICAL':
      return 'var(--critical)';
    default:
      return 'var(--text-muted)';
  }
};

export const getRiskBackgroundColor = (riskLevel) => {
  switch (riskLevel?.toUpperCase()) {
    case 'LOW':
      return 'rgba(16, 185, 129, 0.1)';
    case 'MEDIUM':
      return 'rgba(245, 158, 11, 0.1)';
    case 'HIGH':
      return 'rgba(239, 68, 68, 0.1)';
    case 'CRITICAL':
      return 'rgba(147, 51, 234, 0.1)';
    default:
      return 'rgba(107, 114, 128, 0.1)';
  }
};

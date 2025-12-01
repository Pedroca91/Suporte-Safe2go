-- Schema PostgreSQL para Sistema Safe2Go Helpdesk
-- Criado em: 2025-11-27

-- Extensão para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'cliente', -- 'cliente' ou 'administrador'
    status VARCHAR(50) NOT NULL DEFAULT 'pendente', -- 'pendente', 'aprovado', 'rejeitado'
    phone VARCHAR(50),
    company VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE,
    approved_by UUID
);

-- Tabela de Chamados/Cases
CREATE TABLE IF NOT EXISTS cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    jira_id VARCHAR(50) UNIQUE,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    responsible VARCHAR(255),
    creator_id UUID REFERENCES users(id),
    creator_name VARCHAR(255),
    status VARCHAR(100) NOT NULL DEFAULT 'Pendente',
    priority VARCHAR(50) DEFAULT 'Média',
    seguradora VARCHAR(100),
    category VARCHAR(100),
    keywords TEXT[], -- Array de palavras-chave
    opened_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    closed_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Comentários
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    user_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Notificações
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    case_title VARCHAR(500),
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'new_comment', 'status_change', 'case_assigned'
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Atividades
CREATE TABLE IF NOT EXISTS activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    responsible VARCHAR(255) NOT NULL,
    activity VARCHAR(500) NOT NULL,
    time_spent INTEGER DEFAULT 0, -- minutos
    notes TEXT,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);

CREATE INDEX IF NOT EXISTS idx_cases_creator_id ON cases(creator_id);
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_seguradora ON cases(seguradora);
CREATE INDEX IF NOT EXISTS idx_cases_jira_id ON cases(jira_id);
CREATE INDEX IF NOT EXISTS idx_cases_created_at ON cases(created_at);

CREATE INDEX IF NOT EXISTS idx_comments_case_id ON comments(case_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_is_internal ON comments(is_internal);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read);
CREATE INDEX IF NOT EXISTS idx_notifications_case_id ON notifications(case_id);

CREATE INDEX IF NOT EXISTS idx_activities_case_id ON activities(case_id);

-- Trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_cases_updated_at BEFORE UPDATE ON cases
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

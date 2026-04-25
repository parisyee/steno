create table transcription_attempts (
    id               uuid primary key default gen_random_uuid(),
    created_at       timestamptz not null default now(),
    filename         text,
    file_size_bytes  bigint,
    content_type     text,
    transcribe_model text,
    analyze_model    text,
    skip_trim        boolean,
    polish           boolean,
    status           text not null check (status in ('success', 'failure')),
    error_stage      text,
    error_type       text,
    error_detail     text,
    duration_ms      integer,
    transcription_id uuid references transcriptions(id) on delete set null
);

create index transcription_attempts_created_at_idx on transcription_attempts (created_at desc);
create index transcription_attempts_status_idx     on transcription_attempts (status);
create index transcription_attempts_error_type_idx on transcription_attempts (error_type) where error_type is not null;

CREATE INDEX pollster_pollvote_date_created USING BTREE ON pollster_pollvote(date_created);

CREATE INDEX pollster_poll_date_created USING BTREE ON pollster_poll(date_created);
CREATE INDEX pollster_poll_date_modified USING BTREE ON pollster_poll(date_modified);
CREATE INDEX pollster_poll_total_votes USING BTREE ON pollster_poll(total_votes);
CREATE INDEX pollster_poll_total_comments USING BTREE ON pollster_poll(total_comments);

CREATE INDEX threadedcomments_threadedcomment_date_modified USING BTREE ON threadedcomments_threadedcomment(date_modified);

CREATE INDEX pollster_tag_poll_count USING BTREE ON pollster_tag(poll_count);